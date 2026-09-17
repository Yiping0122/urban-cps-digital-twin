# Manuscript Screenshot Checklist

## 1. Authoritative application

- Public application: <https://urban-health-cps-twin.streamlit.app/>
- Application entry point: `app_command_center.py`
- Screenshot role: implementation evidence for the operator-facing command-center demonstrator.
- Evidence boundary: screenshots demonstrate that interface states and advisory workflow components are implemented and visible. They are not analytical validation, deployment validation, operator-performance evidence, or evidence of measured intervention effects.

## 2. Global pre-capture checks

Complete these checks before capturing any manuscript screenshot:

- [ ] The public deployment reflects the current repository revision.
- [ ] The page is refreshed and no Streamlit asset-loading or image-module error is visible.
- [ ] The sidebar reads `CPS Workflow State: ACTIVE`, not `CPS Synchronization: ACTIVE`.
- [ ] The outcome section is titled `Advisory Outcome Simulation`.
- [ ] Priority rankings use ordinal labels (`High`, `Medium–High`, `Medium`, or `Low`) rather than percentages.
- [ ] The note `Rule-based advisory ranking; not a calibrated probability.` is visible where ranking is shown.
- [ ] No `8–12%` reduction claim or other numerical intervention-effect claim is visible.
- [ ] Expected outcomes are qualitative and marked as simulated or not empirically validated.
- [ ] The interface does not claim live sensing, direct actuation, clinical prediction, measured intervention effectiveness, or validated user-feedback adaptation.
- [ ] The browser zoom, viewport size, sidebar state, and page width are consistent across S1–S4.
- [ ] Personal browser UI, account details, notifications, and unrelated tabs are excluded from the captured frame.

## 3. Scenario screenshot matrix

### S1 Household

Recommended capture: Command Center with `S1 Household` selected.

- [ ] Global scenario selector visibly shows `S1 Household`.
- [ ] Household state and health-aware interpretation are visible.
- [ ] The scene shows scenario-specific window-opening sensing, indoor sensing, ventilation/filtration, or appliance-scheduling context.
- [ ] Priority ranking is ordinal and includes its rule-based-ranking disclaimer.
- [ ] Advisory outcome is qualitative, such as reduced peak-demand pressure, and is labelled as simulated/not empirically validated.
- [ ] Do not frame predictive-fit metrics as evidence of demand reduction or intervention effectiveness.

Manuscript-safe description: The interface makes visible the S1 household interpretation state and its mapping to advisory demand-shifting and indoor-context responses.

### S2 Community

Recommended capture: Command Center with `S2 Community` selected.

- [ ] Global scenario selector visibly shows `S2 Community`.
- [ ] Community demand-monitoring state and aggregation context are visible.
- [ ] Community demand hotspots or aggregation-pressure areas are represented as schematic, not measured geographic hotspots.
- [ ] Community demand coordination, peak-load monitoring, and exposure monitoring are shown as advisory endpoints.
- [ ] Priority ranking is ordinal and includes its rule-based-ranking disclaimer.
- [ ] Advisory outcome is qualitative, such as more balanced load distribution, and is labelled as simulated/not empirically validated.

Manuscript-safe description: The interface demonstrates implementation of community-scale state interpretation and advisory response orchestration.

### S3 Multi-Stressor

Recommended captures: Command Center plus S3 Analysis/Scenario Runtime view.

- [ ] Global scenario selector visibly shows `S3 Multi-Stressor`.
- [ ] PM2.5 and temperature are represented as coupled environmental stressors.
- [ ] Thresholds, when displayed, are identified as distribution-based demonstrator thresholds rather than regulatory or clinical limits.
- [ ] The runtime trigger uses 90th-percentile thresholds.
- [ ] Any archived analytical sample description retains the 90th-percentile rule with 85th-percentile fallback.
- [ ] The 300 rows are described as qualifying samples, not one continuous physical episode.
- [ ] Ventilation/filtration, passive cooling, occupancy advisory, and demand response remain advisory endpoints.
- [ ] Priority ranking is ordinal and includes its rule-based-ranking disclaimer.
- [ ] The expected outcome is qualitative and is labelled as simulated/not empirically validated.

Manuscript-safe description: The interface represents the S3 compound PM2.5–heat state and its traceable mapping to prioritised advisory responses.

### S4 Weather–Air-Quality Sensitivity

Recommended captures: Command Center plus S4 Analysis view.

- [ ] Global scenario selector visibly shows `S4 Weather-AQ`.
- [ ] The command-center state is presented as sensitivity/trade-off exploration.
- [ ] Real heatmap and SHAP figures, where displayed, are treated as qualitative figure-only evidence.
- [ ] `metrics_placeholder.csv`, `prediction_grid_placeholder.csv`, and any placeholder SHAP-summary CSV are visibly identified as documented placeholders.
- [ ] Placeholder CSVs are not used to report numerical sensitivity, accuracy, or performance claims.
- [ ] Priority ranking is ordinal and includes its rule-based-ranking disclaimer.
- [ ] Advisory outcome is qualitative, such as more robust scenario planning, and is labelled as simulated/not empirically validated.

Manuscript-safe description: The interface makes visible a qualitative weather–air-quality sensitivity exploration while clearly separating real figure evidence from placeholder tabular assets.

## 4. Cross-page implementation captures

Capture only where each image adds distinct implementation evidence:

- [ ] **CDE / Digital Thread:** source registration, 15-minute harmonisation, coverage indicator, and traceable state construction.
- [ ] **Analysis:** representative real S1/S2/S3 predictive-fit outputs; S4 must retain its figure-only/placeholder boundary.
- [ ] **Intervention & Feedback Layer:** trigger-to-response mapping, endpoint abstraction, ordinal priority, operator review, and simulated feedback closure.
- [ ] **Smart Healing Interface:** simplified human-facing physical–digital context and top advisory actions; avoid duplicating detailed intervention logic.
- [ ] **Decision Support:** operator-facing review and advisory override choices, without implying autonomous control.

## 5. Caption rules

Use verbs such as `makes visible`, `represents`, and `demonstrates implementation of` for screenshot evidence.

Do not use screenshot captions to claim:

- predictive or clinical validation;
- real-time sensing or deployed synchronization;
- direct HVAC, BEMS, IoT, or device actuation;
- measured exposure, energy, or thermal-stress reduction;
- calibrated intervention probabilities;
- validated operator performance or user-feedback adaptation.

Every screenshot caption should identify the selected scenario, the visible workflow stage, and the advisory/simulated status of the output.

## 6. Local verification record

Local verification against `http://localhost:8502/` confirmed on 17 September 2026:

- [x] S1 Household rendered with ordinal priority labels and a qualitative advisory outcome.
- [x] S2 Community rendered with scenario-specific community monitoring and ordinal priority labels.
- [x] S3 Multi-Stressor rendered with compound PM2.5 and heat interpretation and advisory endpoints.
- [x] S4 Weather-AQ rendered with sensitivity framing; the Analysis page visibly marked the metrics and prediction-grid CSVs as documented placeholders.
- [x] `CPS Workflow State: ACTIVE` replaced the former synchronization wording.
- [x] `Advisory Outcome Simulation` replaced the former impact-simulation wording.
- [x] The interface displayed the ranking disclaimer and no empirical intervention-effect percentage.

The public deployment must be rechecked after the revised code is deployed. Existing earlier screenshots remain historical interface evidence and should not be used to substantiate the revised wording until they are replaced.
