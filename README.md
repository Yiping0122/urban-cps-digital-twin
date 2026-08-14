# MBSE-CPS UrbanEnergyAQ Digital Twin Demonstrator

This Streamlit MVP is an academic prototype for demonstrating how secondary datasets can be integrated into a simulated cyber-physical digital twin workflow.

The dashboard uses the standardized asset layer in `data/`, `outputs/`, and `figures/`. It does not retrain models. Missing files are reported inside the interface as warnings rather than causing the app to crash.

## Dashboard Sections

- **System Overview**: Seven MBSE-CPS modules, data source cards, and demonstrator status.
- **Data Fusion / CDE**: Summary and plots for `community_pm25_weather_merged.csv`.
- **S1 Household Analysis**: House 1 end-use table, daily profile/end-use figures, surrogate metrics, prediction, and SHAP figures.
- **S2 Community Surrogate**: Community surrogate metrics, daily profiles, prediction, and SHAP figures.
- **Scenario Engine / S3 Placeholder**: Displays S3 result files when present, otherwise explains the placeholder episode-detection workflow.
- **Scenario S4**: Displays the PM2.5-temperature sensitivity outputs and documented placeholder CSVs when tabular outputs are unavailable.
- **Decision Support**: Rule-based mock advisory outputs for high PM2.5, high temperature, high load, and SHAP explainability.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dashboard Assets

The app reads only from:

- `data/`
- `outputs/`
- `figures/`

See `README_dashboard_assets.md` for the source and status of every dashboard-ready file.

This is a simulated advisory feedback loop, not a fully deployed real-time control system.

## GitHub Pages Static Site

This repository also includes a static GitHub Pages version in:

```text
docs/index.html
```

The static page is designed for easy sharing and academic demonstration. It does not run the Streamlit Python backend, retrain models, perform live sensing, or actuate devices. It presents the same project logic as a browser-only demonstrator using HTML, CSS, JavaScript, and copied figure assets.

To publish it on GitHub Pages:

1. Push this repository to GitHub.
2. Open the repository on GitHub.
3. Go to **Settings** -> **Pages**.
4. Under **Build and deployment**, set:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
5. Save.

GitHub will provide a URL similar to:

```text
https://Yiping0122.github.io/urban-cps-digital-twin/
```

To update the website later, edit files under `docs/`, commit the changes, and push to GitHub. GitHub Pages will rebuild automatically.

For the newer command-center Streamlit prototype, run:

```bash
streamlit run app_command_center.py --server.port 8502
```

## Streamlit Community Cloud Deployment

The full dynamic command-center prototype should be deployed with Streamlit Community Cloud rather than GitHub Pages.

Recommended Streamlit Cloud settings:

```text
Repository: Yiping0122/urban-cps-digital-twin
Branch: main
Main file path: app_command_center.py
```

This deployment preserves the Streamlit interactions that the static GitHub Pages site cannot provide, including:

- global scenario selector
- Intervention Logic & Response Layer controls
- Operator Review / Advisory Override selections
- Occupant Feedback / Preference Input
- Streamlit session state
- dynamic warning/status rendering for missing files

The GitHub Pages version remains available as a static presentation site. The Streamlit Cloud deployment should be used for the full interactive dashboard.
