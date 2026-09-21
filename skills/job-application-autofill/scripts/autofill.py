#!/usr/bin/env python3
"""Offline, standard-library-only application planner. Never controls a browser.

Inputs are private JSON supplied by the operator from observed UI and confirmed
sources. Output contains personal data: write it only to a private workspace.
"""
import argparse
import copy
import hashlib
import json
import os
import re
from collections import Counter
from datetime import date
from pathlib import Path


def norm(value):
    return re.sub(r"\s+", " ", str(value).strip().rstrip("* ")).casefold()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def pointer(data, path):
    if not path.startswith("/"):
        raise ValueError("Source path must be a JSON pointer")
    for key in path.split("/")[1:]:
        key = key.replace("~1", "/").replace("~0", "~")
        data = data[int(key)] if isinstance(data, list) else data[key]
    return data


def source_value(rule, sources):
    ref = rule["source"]
    if re.search(r"password|secret|token|credential|otp", ref["pointer"], re.I):
        raise ValueError("Credential sources are forbidden")
    value = pointer(sources[ref["name"]], ref["pointer"])
    if value is None or value == "":
        raise ValueError("Confirmed source is missing")
    source_hash = digest(value)
    if "source_sha256" in rule and rule["source_sha256"] != source_hash:
        raise ValueError("Source changed; mapping needs review")
    if "value_map" in rule:
        key = json.dumps(value) if isinstance(value, bool) else str(value)
        if key not in rule["value_map"]:
            raise ValueError("Source value has no confirmed mapping")
        value = rule["value_map"][key]
    if not isinstance(value, (str, int, float, bool)):
        raise ValueError("Source must be scalar; bind repeated groups explicitly")
    return str(value), source_hash


def in_scope(rule, context, field):
    scope = rule.get("scope", {})
    return all(norm((field if key == "group_key" else context).get(key, "")) == norm(value)
               for key, value in scope.items())


def rank_evidence(query, evidence, context):
    """Deterministic retrieval only; ranking is not proof of claim validity."""
    terms = set(re.findall(r"[a-z0-9]+", query.lower())) - {
        "a", "an", "the", "and", "or", "of", "in", "to", "your", "you", "have", "how", "what"}
    ranked = []
    for item in evidence:
        if item.get("status") not in {"confirmed", "experimental", "in-progress"}:
            continue
        if item.get("excluded_from_applications") or not item.get("source_ref"):
            continue
        if item.get("scope") and not in_scope(item, context, {}):
            continue
        bag = Counter(re.findall(r"[a-z0-9]+", " ".join([
            item["title"], " ".join(item.get("tags", [])), item.get("summary", "")]).lower()))
        score = sum(min(bag[t], 3) for t in terms)
        if score:
            ranked.append((score, item["id"], item))
    return [item for _, _, item in sorted(ranked, key=lambda x: (-x[0], x[1]))[:4]]


def plan(manifest, config, sources, today=None):
    today = today or date.today().isoformat()
    context = manifest["context"]
    fields = manifest["fields"]
    ids = [f["id"] for f in fields]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate observed field IDs")
    result = []
    for field in fields:
        item = {"field_id": field["id"], "label": field["label"],
                "required": field.get("required", False), "action": "unresolved"}
        if field.get("visible") is False or field.get("disabled") or field.get("readonly"):
            item.update(action="skip", reason="Not an editable visible control")
            result.append(item)
            continue
        matches = [r for r in config["rules"] if r.get("confirmed") and
                   norm(field["label"]) in {norm(a) for a in r["aliases"]} and
                   in_scope(r, context, field)]
        # A specific employer/group binding overrides a general alias. Equally
        # specific conflicting rules stay unresolved, never pick by file order.
        if matches:
            specificity = max(len(r.get("scope", {})) for r in matches)
            matches = [r for r in matches if len(r.get("scope", {})) == specificity]
        if len(matches) > 1:
            item["reason"] = "Conflicting equally specific rules"
        elif not matches:
            if field.get("kind") == "essay":
                item.update(action="reason", evidence=rank_evidence(
                    field["label"] + " " + context.get("role", "") + " " + context.get("job_keywords", ""),
                    config.get("evidence", []), context),
                    writing_rules=config.get("writing_rules", []),
                    word_limit=field.get("word_limit"), char_limit=field.get("char_limit"),
                    employer_ai_rules=manifest.get("employer_ai_rules", "Inspect before drafting"))
            else:
                item["reason"] = "No exact confirmed rule; classify or retrieve the missing fact"
        else:
            rule = matches[0]
            item["rule_id"] = rule["id"]
            if rule.get("expires_on", "9999-12-31") < today:
                item["reason"] = "Time-dependent answer expired"
            elif rule.get("gate"):
                item.update(action="permission", reason=rule["gate"])
            elif field.get("user_edited"):
                item.update(action="keep", reason="Preserve current user edit; inspect any factual conflict")
            else:
                try:
                    value, source_hash = source_value(rule, sources)
                    if rule.get("compare") == "phone" and field.get("separate_dial_code"):
                        prefix = re.sub(r"\D", "", str(field["separate_dial_code"]))
                        digits = re.sub(r"\D", "", value)
                        if value.startswith("+") and prefix and digits.startswith(prefix):
                            value = digits[len(prefix):]
                    item.update(source=rule["source"], source_sha256=source_hash, value=value)
                    visibility = field.get("value_state", "unknown")
                    if visibility not in {"known", "empty", "unknown", "redacted"}:
                        raise ValueError("Invalid value_state")
                    if visibility in {"unknown", "redacted"}:
                        item.update(action="inspect", reason="Missing UI value is not an empty field")
                    elif visibility == "known" and (
                        (re.sub(r"\D", "", str(field.get("value", ""))) == re.sub(r"\D", "", value))
                        if rule.get("compare") == "phone" else norm(field.get("value", "")) == norm(value)
                    ):
                        item.update(action="keep", reason="Already matches confirmed answer")
                    elif field.get("kind") == "select":
                        allowed = {norm(v) for v in [value] + rule.get("option_aliases", [])}
                        options = [o for o in field.get("options", []) if norm(o) in allowed]
                        if len(options) == 1:
                            item.update(action="select", value=options[0])
                        else:
                            item.update(action="inspect-options", reason="Observe one exact supported option")
                    elif field.get("kind") == "text":
                        item.update(action="replace", method="fill")
                    else:
                        item.update(action="inspect", reason="Control needs a supported adapter")
                except (KeyError, IndexError, TypeError, ValueError) as error:
                    item.pop("value", None)
                    item.update(action="unresolved", reason=str(error))
        result.append(item)
    batches = []
    for field, item in zip(fields, result):
        locator = field.get("locator", {})
        if item["action"] == "replace" and locator.get("by") == "role" and locator.get("role") == "textbox" and locator.get("name") == field["label"] and field.get("locator_unique") is True:
            batches.append({"field_id": field["id"], "method": "fill", "name": locator["name"], "value": item["value"]})
    # JSON escaping prevents user data from becoming executable JavaScript.
    # The operator must bind `applicationTab` to the verified live tab and check
    # current permissions/state. This output never executes itself.
    code = ["// Verify current tab, manifest, sources and host authorization before execution."]
    for item in batches:
        code.append("await applicationTab.playwright.getByRole('textbox', {name: " + json.dumps(item["name"]) + ", exact: true}).fill(" + json.dumps(item["value"]) + ");")
    if batches:
        code.append("await applicationTab.getAXState();")
    return {"version": 1, "context": context, "manifest_sha256": digest(manifest),
            "config_sha256": digest(config), "submission": "never performed by this helper",
            "summary": dict(Counter(i["action"] for i in result)), "fields": result,
            "text_batch": batches, "cua_text_batch": "\n".join(code)}


def check_answer(answer, evidence, forbidden_phrases=()):
    """Mechanical checks only; a human/agent must still verify every claim."""
    text = answer["text"]
    issues = []
    if answer.get("word_limit") and len(text.split()) > answer["word_limit"]:
        issues.append("word_limit")
    if answer.get("char_limit") and len(text) > answer["char_limit"]:
        issues.append("char_limit")
    for phrase in forbidden_phrases:
        if norm(phrase) in norm(text):
            issues.append("excluded_topic:" + phrase)
    index = {e["id"]: e for e in evidence if not e.get("excluded_from_applications")}
    for claim in answer.get("claims", []):
        if not claim.get("evidence_ids") or any(i not in index for i in claim["evidence_ids"]):
            issues.append("missing_evidence:" + claim.get("text", ""))
    if not answer.get("claims"):
        issues.append("claim_ledger_missing")
    return {"mechanical_checks_passed": not issues, "issues": issues,
            "semantic_claim_review_required": True}


def learn_alias(request, config, sources):
    """Remember reviewed wording for an existing fact; never create new facts.

    Semantic review is performed by the operator against the current question.
    This function only enforces source, context, conflict and scope invariants.
    """
    manifest = request["manifest"]
    if request.get("manifest_sha256") != digest(manifest):
        raise ValueError("Review does not match the observed manifest")
    if request.get("semantic_equivalence_reviewed") is not True or not request.get("review_note", "").strip():
        raise ValueError("Review exact wording, negation, jurisdiction and meaning first")
    fields = [f for f in manifest["fields"] if f["id"] == request["field_id"]]
    matches = [r for r in config["rules"] if r["id"] == request["rule_id"]]
    if len(fields) != 1 or len(matches) != 1:
        raise ValueError("Field and existing rule must be unambiguous")
    field, rule = fields[0], matches[0]
    if field.get("kind") not in {"text", "select"} or field.get("visible") is False:
        raise ValueError("Only observed routine field wording can be learned")
    if not rule.get("confirmed") or not in_scope(rule, manifest["context"], field):
        raise ValueError("Existing rule is not confirmed for this context")
    if rule.get("expires_on", "9999-12-31") < date.today().isoformat():
        raise ValueError("Existing answer has expired")
    if rule.get("gate"):
        raise ValueError("Disclosure and permission wording must be reviewed separately")
    source_value(rule, sources)
    alias = field["label"].strip()
    if not alias:
        raise ValueError("Empty label")
    # Never introduce an alias already owned by another rule, even if that
    # rule is currently out of scope. Resolve the overlap explicitly instead.
    for other in config["rules"]:
        if other["id"] != rule["id"] and norm(alias) in map(norm, other["aliases"]):
            raise ValueError("This wording already belongs to another rule")
    updated = copy.deepcopy(config)
    target = next(r for r in updated["rules"] if r["id"] == rule["id"])
    if norm(alias) not in map(norm, target["aliases"]):
        target["aliases"].append(alias)
        updated.setdefault("alias_history", []).append({
            "rule_id": rule["id"], "alias": alias, "date": date.today().isoformat(),
            "context": manifest["context"], "review_note": request["review_note"],
            "manifest_sha256": request["manifest_sha256"]})
    return updated


def write_private(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as out:
        json.dump(data, out, indent=2)
        out.write("\n")
    path.chmod(0o600)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["plan", "check-answer", "learn-alias"])
    ap.add_argument("--config", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text())
    payload = json.loads(Path(args.input).read_text())
    if args.command in {"plan", "learn-alias"}:
        sources = {name: json.loads((config_path.parent / path).read_text())
                   for name, path in config["sources"].items()}
        output = plan(payload, config, sources) if args.command == "plan" else learn_alias(payload, config, sources)
    else:
        output = check_answer(payload, config.get("evidence", []), config.get("forbidden_phrases", []))
    if Path(args.output).resolve() == config_path:
        if args.command != "learn-alias":
            raise ValueError("Only learn-alias can replace the configuration")
        write_private(str(config_path) + '.before-alias.json', config)
    write_private(args.output, output)
    # Keep personal values out of terminal summaries.
    if args.command == "learn-alias":
        print(json.dumps({"rules": len(output["rules"]), "aliases": sum(len(r["aliases"]) for r in output["rules"])}))
    else:
        print(json.dumps(output.get("summary", {k: v for k, v in output.items() if k != "fields"})))


if __name__ == "__main__":
    main()
