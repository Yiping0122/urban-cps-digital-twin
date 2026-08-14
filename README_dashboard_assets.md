# Dashboard Asset Layer

This file documents the lightweight, dashboard-ready output layer for the Streamlit MBSE-CPS UrbanEnergyAQ demonstrator.

Original research scripts and source datasets are not deleted or overwritten. The dashboard reads only from:

- `data/`
- `outputs/`
- `figures/`

## Asset Inventory

| Dashboard file | Source | Status | Mapping |
|---|---|---:|---|
| `data/community_pm25_weather_merged.csv` | `ukdale/community_pm25_weather_merged.csv` | Real output | M1-M2, CDE data fusion |
| `outputs/s1/house1_enduse_energy_kwh.csv` | `ukdale/fig_s1_behavior/house1_enduse_energy_kwh.csv` | Real output | M3, S1 household end-use analysis |
| `outputs/s1/metrics.csv` | `ukdale/fig_s1_surrogate/table3_s1_surrogate_metrics.csv` | Real output | M4, S1 surrogate evaluation |
| `outputs/s1/predictions_placeholder.csv` | No prediction CSV found; existing evidence is `figures/s1/fig5a_pred_vs_actual.png` | Placeholder | M4, S1 prediction output |
| `outputs/s1/shap_summary_placeholder.csv` | No SHAP CSV found; existing evidence is `figures/s1/fig5b_shap_summary.png` | Placeholder | M7, S1 explainability |
| `outputs/s2/metrics.csv` | `ukdale/fig_s2_community/table4_community_metrics.csv` | Real output | M4, S2 community surrogate evaluation |
| `outputs/s2/predictions_placeholder.csv` | No prediction CSV found; existing evidence is `figures/s2/fig6b_pred_vs_actual.png` and `figures/s2/fig9a_city_surrogate_pred_vs_actual.png` | Placeholder | M4, S2 prediction output |
| `outputs/s2/shap_summary_placeholder.csv` | No SHAP CSV found; existing evidence is `figures/s2/fig6c_shap.png` and `figures/s2/fig9b_city_surrogate_shap.png` | Placeholder | M7, S2 explainability |
| `outputs/s3/episode_results.csv` | `ukdale/s3_episode_with_preds.csv` | Real output | M6, S3 high PM2.5 plus high temperature episode |
| `outputs/s3/metrics.csv` | Derived from `outputs/s3/episode_results.csv` without retraining | Real derived output | M4-M6, S3 episode evaluation |
| `outputs/s3/event_summary.csv` | Derived from `outputs/s3/episode_results.csv` without retraining | Real derived output | M6-M7, S3 scenario summary |
| `outputs/s4/prediction_grid_placeholder.csv` | No S4 prediction-grid CSV found; existing evidence is `figures/s4/fig10_s4_pm25_temp_heatmap.png` | Placeholder | M6, S4 PM2.5-temperature sensitivity |
| `outputs/s4/metrics_placeholder.csv` | No S4 metrics CSV found | Placeholder | M4-M6, S4 evaluation |
| `outputs/s4/shap_summary_placeholder.csv` | No S4 SHAP CSV found; existing evidence is `figures/s4/fig10a_shap_no_weather.png` and `figures/s4/fig10b_shap_weather.png` | Placeholder | M7, S4 explainability |

## Figure Inventory

| Dashboard file | Source figure | Status | Mapping |
|---|---|---:|---|
| `figures/framework/fig7a_load_pm25_trend.png` | `fig7a_load_pm25_trend.png` | Real figure | M1-M2, energy-air-quality trend |
| `figures/framework/fig7b_surrogate_prediction.png` | `fig7b_surrogate_prediction.png` | Real figure | M4, surrogate prediction |
| `figures/framework/fig7c_shap_importance.png` | `fig7c_shap_importance.png` | Real figure | M7, explainability |
| `figures/framework/fig8a_pm25_bins_load.png` | `ukdale/fig8a_pm25_bins_load.png` | Real figure | M5, PM2.5-load relationship |
| `figures/framework/fig8b_rolling_trend.png` | `ukdale/fig8b_rolling_trend.png` | Real figure | M5, rolling environmental trend |
| `figures/framework/fig8c_pm25_load_ccf.png` | `ukdale/fig8c_pm25_load_ccf.png` | Real figure | M5, cross-correlation |
| `figures/s1/fig4a_house1_daily_profiles.png` | `ukdale/fig_s1_behavior/fig4a_house1_daily_profiles.png` | Real figure | M3, S1 household profile |
| `figures/s1/fig4b_house1_enduse_shares.png` | `ukdale/fig_s1_behavior/fig4b_house1_enduse_shares.png` | Real figure | M3, S1 end-use shares |
| `figures/s1/fig5a_pred_vs_actual.png` | `ukdale/fig_s1_surrogate/fig5a_pred_vs_actual.png` | Real figure | M4, S1 prediction |
| `figures/s1/fig5b_shap_summary.png` | `ukdale/fig_s1_surrogate/fig5b_shap_summary.png` | Real figure | M7, S1 explainability |
| `figures/s2/fig6a_daily_profiles.png` | `ukdale/fig_s2_community/fig6a_daily_profiles.png` | Real figure | M4, S2 community profile |
| `figures/s2/fig6b_pred_vs_actual.png` | `ukdale/fig_s2_community/fig6b_pred_vs_actual.png` | Real figure | M4, S2 prediction |
| `figures/s2/fig6c_shap.png` | `ukdale/fig_s2_community/fig6c_shap.png` | Real figure | M7, S2 explainability |
| `figures/s2/fig9a_city_surrogate_pred_vs_actual.png` | `ukdale/fig9a_city_surrogate_pred_vs_actual.png` | Real figure | M4, city-scale surrogate |
| `figures/s2/fig9b_city_surrogate_shap.png` | `ukdale/fig9b_city_surrogate_shap.png` | Real figure | M7, city-scale explainability |
| `figures/s3/fig10_s3a_highstress_load_pred.png` | `ukdale/fig10_s3a_highstress_load_pred.png` | Real figure | M6, S3 episode prediction |
| `figures/s3/fig10_s3b_highstress_env.png` | `ukdale/fig10_s3b_highstress_env.png` | Real figure | M5-M6, S3 PM2.5-temperature episode |
| `figures/s4/fig10_s4_pm25_temp_heatmap.png` | `ukdale/fig10_s4_pm25_temp_heatmap.png` | Real figure | M6, S4 counterfactual sensitivity |
| `figures/s4/fig10a_shap_no_weather.png` | `ukdale/shap_compare/fig10a_shap_no_weather.png` | Real figure | M7, explainability without weather |
| `figures/s4/fig10b_shap_weather.png` | `ukdale/shap_compare/fig10b_shap_weather.png` | Real figure | M7, explainability with weather |

## Module and Scenario Mapping

M1 acquires secondary energy, PM2.5, and weather data. M2 harmonises those data into the CDE table in `data/`. M3 describes household behaviour through S1 end-use outputs. M4 hosts the S1 and S2 surrogate evaluation outputs. M5 supplies environmental context and PM2.5-weather interpretation figures. M6 organises S3 and S4 scenario outputs. M7 turns prediction and SHAP evidence into advisory/explainability material.

S1 maps to `outputs/s1/` and `figures/s1/`. S2 maps to `outputs/s2/` and `figures/s2/`. S3 maps to `outputs/s3/` and `figures/s3/`. S4 maps to `outputs/s4/` and `figures/s4/`.

Placeholder files are intentionally retained so the dashboard has stable schemas while making gaps visible. They should be replaced by real model-output CSVs when those files become available.
