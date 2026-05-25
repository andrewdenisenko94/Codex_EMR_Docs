# Input Schema (Markdown/JSON-friendly)

## Top-level fields
- patient: name_placeholder, dob_placeholder, mrn_placeholder, age, sex, gestational_age
- encounter: date, time, location_service, requesting_team, attending, consult_reason
- gu_history: diagnoses, congenital_anatomy, prior_gu_surgeries, uti_history, stones, vur, utd_hn, neurogenic_bladder, devices
- presentation: symptoms, vitals, fever, pain, emesis, hematuria, retention, scrotal_findings, trauma_mechanism
- voiding: spontaneous_voiding, pvr_values, bladder_scan, cic_regimen, foley_status_size, urine_character
- infection: antibiotics, prophylaxis, ua_lines, ucx_lines, bcx_lines, colonization_vs_infection
- labs: cr, wbc, hgb, bun, inflammatory_markers
- imaging: dated_modality_findings[] with laterality and measurements
- procedures: dated_procedures[] with findings/devices/complications
- assessment: acute_issue, obstruction_status, infection_status, intervention_rationale
- plan: actions[], follow_up, return_precautions
- uncertainties: missing_data[], contradictions[]
