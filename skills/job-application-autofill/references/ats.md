# ATS interaction recipes

These are starting hypotheses, not hard-coded selectors. Inspect each current page and read tool documentation before using an API.

## Greenhouse

- Usually one long form with custom dropdowns, optional repeated education groups, resume and cover-letter upload controls, and employer questions.
- Scope similarly named controls. Country and location may be asynchronous selectors; wait for results and click the observed exact option.
- Contact values can be omitted from accessibility/read-only DOM output. Check the rendered field before assuming it is empty.
- For upload, arm the supported file-chooser event, click the visible Resume Attach button, then set the verified local PDF. Do not repeatedly click a hidden input. Confirm the filename appears and upload completes.

## Ashby

- Inventory employer-specific questions; identical ATS does not mean identical application requirements.
- Distinguish checkbox groups from single-choice questions; inspect all option labels and selected states.
- Verify uploaded filename and any subsequent resume-parsed changes. Keep applicant-written answers unless correction is authorized/needed.

## Workday

- Check employer tenant/account context. Use normal password-manager autofill without exposing credentials; different tenant may need a separate account.
- Reconcile resume-parsed education/employment once before manual additions. Work section by section and re-inspect each new page.
- Save/resume navigation is not submission; verify final receipt independently.

## Unsupported or changed forms

Use the same confirmed profile through supported visible controls. Do not invent selectors, query private state, or bypass a security block. After repeated failure, retain completed work, document the exact unresolved control, and request only the necessary user action.
