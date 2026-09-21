import copy
import unittest
from autofill import plan, check_answer, learn_alias, digest


class AutofillTests(unittest.TestCase):
    def setUp(self):
        self.sources = {"profile": {"email": "person@example.test", "authorized": True}}
        self.config = {"rules": [{"id": "email", "aliases": ["Email", "Email address"],
            "confirmed": True, "source": {"name": "profile", "pointer": "/email"}}]}
        self.manifest = {"context": {"company": "Example", "country": "US"}, "fields": [
            {"id": "email", "label": "Email*", "kind": "text", "value_state": "empty"}]}

    def output(self):
        return plan(self.manifest, self.config, self.sources)["fields"][0]

    def test_first_fill_then_repeat_is_noop(self):
        first = self.output()
        self.assertEqual(first["action"], "replace")
        self.manifest["fields"][0].update(value_state="known", value=first["value"])
        self.assertEqual(self.output()["action"], "keep")

    def test_redacted_contact_never_appends(self):
        self.manifest["fields"][0]["value_state"] = "redacted"
        self.assertEqual(self.output()["action"], "inspect")

    def test_existing_duplicate_is_replaced(self):
        self.manifest["fields"][0].update(value_state="known", value="person@example.testperson@example.test")
        self.assertEqual(self.output()["action"], "replace")

    def test_unknown_and_negated_questions_do_not_match(self):
        self.manifest["fields"][0]["label"] = "Do not use this email?"
        self.assertEqual(self.output()["action"], "unresolved")

    def test_country_specific_rule_does_not_transfer(self):
        self.config["rules"][0]["scope"] = {"country": "CA"}
        self.assertEqual(self.output()["action"], "unresolved")

    def test_employer_override_wins(self):
        scoped = copy.deepcopy(self.config["rules"][0])
        scoped.update(id="company-email", scope={"company": "Example"})
        self.config["rules"].append(scoped)
        self.assertEqual(self.output()["rule_id"], "company-email")

    def test_conflicting_rules_fail_closed(self):
        self.config["rules"].append(copy.deepcopy(self.config["rules"][0]))
        self.assertEqual(self.output()["action"], "unresolved")

    def test_dropdown_requires_observed_option(self):
        self.manifest["fields"][0]["kind"] = "select"
        self.assertEqual(self.output()["action"], "inspect-options")
        self.manifest["fields"][0]["options"] = ["person@example.test"]
        self.assertEqual(self.output()["action"], "select")

    def test_user_edit_kept(self):
        self.manifest["fields"][0]["user_edited"] = True
        self.assertEqual(self.output()["action"], "keep")

    def test_hidden_input_skipped(self):
        self.manifest["fields"][0]["visible"] = False
        self.assertEqual(self.output()["action"], "skip")

    def test_formatted_phone_kept(self):
        self.sources["profile"]["email"] = "+1 555-010-2222"
        self.config["rules"][0]["compare"] = "phone"
        self.manifest["fields"][0].update(value_state="known", value="1 (555) 010-2222")
        self.assertEqual(self.output()["action"], "keep")

    def test_separate_dial_code_not_duplicated(self):
        self.sources["profile"]["email"] = "+1 555-010-2222"
        self.config["rules"][0]["compare"] = "phone"
        self.manifest["fields"][0].update(value_state="known", value="(555) 010-2222", separate_dial_code="+1")
        self.assertEqual(self.output()["action"], "keep")
        self.assertEqual(self.output()["value"], "5550102222")

    def test_permission_gate_cannot_be_turned_into_fill(self):
        self.config["rules"][0]["gate"] = "Check host confirmation requirements"
        self.assertEqual(self.output()["action"], "permission")

    def test_duplicate_observed_ids_rejected(self):
        self.manifest["fields"].append(copy.deepcopy(self.manifest["fields"][0]))
        with self.assertRaises(ValueError):
            self.output()

    def test_batch_only_for_observed_unique_text_locator(self):
        self.manifest["fields"][0].update(locator={"by":"role","role":"textbox","name":"Email*"}, locator_unique=True)
        out = plan(self.manifest, self.config, self.sources)
        self.assertEqual(len(out["text_batch"]), 1)
        self.assertIn('.fill(', out["cua_text_batch"])
        self.manifest["fields"][0]["value_state"] = "redacted"
        self.assertEqual(plan(self.manifest, self.config, self.sources)["text_batch"], [])

    def test_education_scoped_group_not_duplicated(self):
        self.config["rules"][0]["scope"] = {"group_key": "college-a"}
        self.manifest["fields"][0]["group_key"] = "college-b"
        self.assertEqual(self.output()["action"], "unresolved")

    def test_source_change_invalidates_mapping(self):
        self.config["rules"][0]["source_sha256"] = "old"
        self.assertEqual(self.output()["action"], "unresolved")

    def test_boolean_false_is_not_missing(self):
        self.sources["profile"]["authorized"] = False
        self.config["rules"][0].update(source={"name": "profile", "pointer": "/authorized"},
                                      value_map={"true": "Yes", "false": "No"})
        self.assertEqual(self.output()["value"], "No")

    def test_credentials_rejected(self):
        self.sources["profile"]["password"] = "fake"
        self.config["rules"][0]["source"]["pointer"] = "/password"
        self.assertEqual(self.output()["action"], "unresolved")

    def test_expired_answer(self):
        self.config["rules"][0]["expires_on"] = "2000-01-01"
        self.assertEqual(self.output()["action"], "unresolved")

    def test_unknown_essay_gets_evidence_not_invented_answer(self):
        self.manifest["fields"][0].update(label="Describe supplier analytics", kind="essay")
        self.config["evidence"] = [
            {"id": "supplier", "title": "Supplier analytics", "status": "confirmed", "source_ref": "private.md"},
            {"id": "excluded", "title": "Supplier analytics", "status": "confirmed", "source_ref": "private.md", "excluded_from_applications": True}]
        out = self.output()
        self.assertEqual(out["action"], "reason")
        self.assertEqual([e["id"] for e in out["evidence"]], ["supplier"])
        self.assertNotIn("value", out)

    def test_answer_check_does_not_claim_semantic_verification(self):
        result = check_answer({"text": "Job searching", "claims": []}, [], ["job searching"])
        self.assertFalse(result["mechanical_checks_passed"])
        self.assertTrue(result["semantic_claim_review_required"])

    def alias_request(self):
        self.manifest["fields"][0]["label"] = "Your email address"
        return {"manifest":self.manifest, "manifest_sha256":digest(self.manifest),
                "field_id":"email", "rule_id":"email", "semantic_equivalence_reviewed":True,
                "review_note":"Observed contact-email question; same meaning as existing email field."}

    def test_learned_wording_uses_existing_fact_next_time(self):
        req = self.alias_request()
        self.config = learn_alias(req, self.config, self.sources)
        self.assertEqual(self.output()["action"], "replace")
        self.assertEqual(self.output()["value"], "person@example.test")
        self.assertEqual(len(self.config["rules"]), 1)

    def test_relearning_alias_is_idempotent(self):
        req = self.alias_request()
        self.config = learn_alias(req, self.config, self.sources)
        self.assertEqual(self.config, learn_alias(req, self.config, self.sources))

    def test_alias_cannot_escape_country_scope(self):
        req = self.alias_request()
        self.config["rules"][0]["scope"] = {"country":"CA"}
        with self.assertRaises(ValueError):
            learn_alias(req, self.config, self.sources)

    def test_alias_requires_review(self):
        req = self.alias_request()
        req["semantic_equivalence_reviewed"] = False
        with self.assertRaises(ValueError):
            learn_alias(req, self.config, self.sources)

    def test_alias_does_not_learn_essay_or_disclosure(self):
        req = self.alias_request()
        self.config["rules"][0]["gate"] = "Permission required"
        with self.assertRaises(ValueError):
            learn_alias(req, self.config, self.sources)

    def test_stale_manifest_cannot_be_learned(self):
        req = self.alias_request()
        req["manifest_sha256"] = "old"
        with self.assertRaises(ValueError):
            learn_alias(req, self.config, self.sources)


if __name__ == "__main__":
    unittest.main()
