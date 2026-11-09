from scripts.auditar_publicacao import is_valid_cpf, scan_numeric_pii


def test_sha256_digest_is_not_reported_as_cpf():
    digest = "99c551e382d5dc41c99419631699c2a19ce4ef3a58d5e12ad0c7041c1586f357"
    findings = []

    digits = [9, 9, 4, 1, 9, 6, 3, 1, 6, 9, 9]
    assert is_valid_cpf("".join(map(str, digits)))
    scan_numeric_pii(f'"sha256": "{digest}"', "manifesto.json", findings)

    assert findings == []


def test_valid_cpf_candidate_in_plain_text_is_still_reported():
    findings = []

    candidate = ".".join(("529", "982", "247")) + "-25"
    scan_numeric_pii(f"CPF: {candidate}", "registro.txt", findings)

    assert [finding.category for finding in findings] == ["cpf"]
