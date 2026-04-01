library(shiny)
library(bslib)
library(plotly)
library(dplyr)
library(DT)
library(scales)

# ==============================================================================
# Azerbaijan CPF / WBG Operations Dashboard
# Full version with:
# - fixed top metric cards (no clipped numbers / internal scroll)
# - fixed Risk Register heatmap labels (reduced overlap)
# ============================================================================== 

# ------------------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------------------

challenges_df <- data.frame(
  challenge = c(
    "Oil dependency",
    "Private sector stagnation",
    "Financial sector vulnerability",
    "Poverty & inequality",
    "Climate & environment",
    "Human capital",
    "Governance"
  ),
  detail = c(
    "Oil and gas account for around 80% of fiscal revenues, 90% of exports, and about one-third of GDP.",
    "The state accounted for 56% of total investment in 2023 and SOEs continue to play a dominant role.",
    "Low bank intermediation, SME access constraints, dollarization risks, and stalled women's financial inclusion.",
    "Poverty fell sharply historically but rural vulnerability remains and social assistance coverage is limited.",
    "Water stress, methane emissions, climate-sensitive agriculture, and broader adaptation pressure remain material.",
    "Learning outcomes remain weak and preschool participation remains relatively low.",
    "Transparency, data quality, and anti-corruption implementation remain important institutional issues."
  ),
  source = c(
    "CPF HLO1/HLO2",
    "CPF HLO2",
    "CPF / Financial sector context",
    "CPF social context",
    "CPF resilience and sustainability",
    "CPF human capital context",
    "CPF governance context"
  ),
  stringsAsFactors = FALSE
)

kpi_df <- data.frame(
  # 最初の7つがHLO1、次の7つがHLO2、最後の1つ(Landowners)はHLO1
  category = c(rep("HLO1", 7), rep("HLO2", 7), "HLO1"),
  objective = c(rep("Resilience & Sustainability", 7), rep("Productivity & Better Jobs", 7), "Resilience & Sustainability"),
  indicator = c(
    "Renewable energy capacity added",
    "Renewable energy share in total capacity",
    "GHG emission reduction",
    "Transformer capacity added to transmission system",
    "Population with access to safe water",
    "Crop yield increase in irrigated lands",
    "Desalinated water processing volume",
    "New / improved jobs created",
    "MSME outstanding loan balance",
    "Loans to women-led SMEs (Bank Respublika)",
    "Vocational training graduates",
    "Beneficiaries of sustainable transport infrastructure",
    "Climate-resilient road development",
    "Broadband internet users",
    "Landowners with irrigation / drainage services"
  ),
  # GHG(3番目)とLandowners(15番目)のNAを0に修正
  baseline = c(0, 20, 0, 0, 0, 0, 0, 0, NA, 14.9, 0, 0, 0, 8.8, 0),
  current = c(0, 20, 0, 0, 0, 0, 0, 0, NA, 14.9, 0, 0, 0, 8.8, 0),
  target = c(0.24, 34, -327000, 1000000, 1.5, 20, 100, 100000, 800, 67, 1300, 100000, 56, 9.4, 146000),
  unit = c(
    "GW", "%", "tCO2eq/year", "kVA", "million people", "%", "million m3",
    "jobs", "USD million", "USD million", "graduates", "people", "km", "million users", "landowners"
  ),
  target_year = c(2029, 2029, 2027, 2027, 2029, 2029, 2029, 2029, 2029, 2029, 2027, 2027, 2026, 2029, 2028),
  note = c(
    "AZURE project",
    "AZURE project",
    "AZURE / climate related SPI",
    "Transmission system upgrade SPI",
    "90% safely managed water standard noted in CPF",
    "Agriculture & irrigation project",
    "Desalination target",
    "Of which 40,000 for women",
    "IFC / private sector mobilization",
    "IFC support",
    "40% women target",
    "Transport connectivity",
    "Transport SPI",
    "Of which women 4.6 million",
    "At least 15% women"
  ),
  stringsAsFactors = FALSE
)

kpi_df$progress_pct <- mapply(function(b, c, t) {
  if (is.na(c) || is.na(t)) return(NA_real_)
  if (!is.na(b) && t != b) return(pmax(0, pmin(100, (c - b) / (t - b) * 100)))
  if (is.na(b) && t != 0) return(NA_real_)
  0
}, kpi_df$baseline, kpi_df$current, kpi_df$target)

pipeline_df <- data.frame(
  project = c(
    "Employment Support Project (Additional Financing)",
    "Azerbaijan Scaling-up Renewable Energy (AZURE)",
    "Competitive, Resilient Agriculture and Irrigation Project",
    "Livable Baku (Urban Regeneration)",
    "CPF Period Total (Estimated)",
    "Current IFC outstanding portfolio",
    "Expected IFC expansion during CPF period"
  ),
  amount_usd_m = c(150, 225, 400, 200, 1250, 47, 350),
  stage = c(
    "Implementation",
    "Preparation",
    "Preparation",
    "Identification",
    "Portfolio envelope",
    "Implementation",
    "Identification"
  ),
  institution = c("IBRD", "IBRD", "IBRD", "IBRD", "IBRD", "IFC", "IFC"),
  focus = c(
    "Jobs / social protection",
    "Energy transition",
    "Agriculture / irrigation",
    "Urban resilience",
    "CPF financing envelope",
    "Financial sector",
    "Financial sector / climate / MSME"
  ),
  fy = c("FY25-26", "FY25-26", "FY25-26", "FY25-26", "FY25-29", "Current", "FY25-29"),
  stringsAsFactors = FALSE
)

cycle_df <- data.frame(
  stage = c(
    "1. Identification",
    "2. Preparation",
    "3. Appraisal",
    "4. Negotiation / Approval",
    "5. Implementation",
    "6. Completion / Validation / Evaluation"
  ),
  what_happens = c(
    "Country priorities and project concept are framed against CPF / SCD priorities.",
    "Technical, fiduciary, environmental, social, and institutional design is developed.",
    "Project design, feasibility, risk, economic logic, and implementation readiness are reviewed.",
    "Project documents are finalized and approval / signing processes are completed.",
    "Borrower executes; Bank supervises; indicators, disbursements, and risks are monitored.",
    "Results, lessons, and effectiveness are reviewed through completion and evaluation documents."
  ),
  repo_relevance = c(
    "Supports baseline diagnostics and Azerbaijan CPF-style strategic framing.",
    "Provides structured indicator tables for macro, climate, jobs, banking, trade, and connectivity analysis.",
    "Supports benchmarking, target framing, and evidence packs for results frameworks.",
    "Provides consistent tables and dashboard-ready summaries for documentation and review.",
    "Feeds periodic monitoring through KPI, budget, lending, reserves, and NPL views.",
    "Supports retrospective review of trends, execution progress, and results interpretation."
  ),
  stringsAsFactors = FALSE
)

budget_df <- data.frame(
  indicator = c("Revenues", "Expenditures", "Fiscal Balance"),
  full_year_2025 = c(39131, 38604, 528),
  jan_2026 = c(3707, 1438, 2270),
  unit = c("mln AZN", "mln AZN", "mln AZN"),
  stringsAsFactors = FALSE
)

loan_trend_df <- data.frame(
  period = c("Dec 2024", "Dec 2025", "Jan 2026"),
  total_loans = c(29288, 31947, 31864),
  private_banks = c(20327, 22196, 22143),
  state_owned_banks = c(7151, 7867, 7837),
  stringsAsFactors = FALSE
)

sector_df <- data.frame(
  sector = c("Household Loans", "Trade and Services", "Transport and Communication", "Industry and Manufacturing", "Construction", "Agriculture"),
  balance = c(18230, 4248, 2164, 1636, 1325, 453),
  share = c(57.1, 13.3, 6.8, 5.1, 4.2, 1.4),
  stringsAsFactors = FALSE
)

macro_cards_df <- data.frame(
  metric = c(
    "Central Bank Foreign Reserves",
    "Broad Money Supply (M3)",
    "Household Deposits",
    "Government Debt (% GDP)",
    "NPL Ratio",
    "IBRD Undisbursed Balance"
  ),
  value = c("US$11.8B", "49,860.3 mln AZN", "16,772.4 mln AZN", "21.8%", "2.6%", "US$176.1M"),
  note = c(
    "Equivalent to 5.7 months of imports",
    "End of 2025",
    "End of 2025",
    "2023 baseline",
    "Jan 2026",
    "As of Dec 2024"
  ),
  stringsAsFactors = FALSE
)

financial_commitments_df <- data.frame(
  category = c(
    "IBRD pipeline envelope (low)",
    "IBRD pipeline envelope (high)",
    "IFC expansion (low)",
    "IFC expansion (high)",
    "Current IFC outstanding portfolio",
    "SOFAZ to IFC AMC managed funds"
  ),
  amount = c(1000, 1500, 200, 500, 47, 350),
  stringsAsFactors = FALSE
)

macro_forecast_df <- data.frame(
  indicator = c("GDP growth", "Non-oil GDP growth", "Inflation", "Current account balance (% GDP)", "Fiscal balance (% GDP)"),
  `2025` = c("1.4%", "2.7%", "5.6%", "14.9%", "+0.4%"),
  `2026` = c("2.6%", "3.2%", "4.8%", "11.5%", "-0.2%"),
  `2027` = c("2.8%", "3.4%", "4.0%", "9.8%", "-0.5%"),
  stringsAsFactors = FALSE
)

risk_df <- data.frame(
  risk_category = c(
    "Political & Governance",
    "Macroeconomic",
    "Sector Strategies & Policies",
    "Technical Design",
    "Institutional Capacity",
    "Fiduciary",
    "Environment & Social",
    "Stakeholders",
    "Overall"
  ),
  rating = c("M", "M", "S", "M", "M", "M", "M", "M", "M"),
  meaning = c("Moderate", "Moderate", "Substantial", "Moderate", "Moderate", "Moderate", "Moderate", "Moderate", "Moderate"),
  stringsAsFactors = FALSE
)

risk_points <- data.frame(
  risk = c(
    "Political & Governance",
    "Macroeconomic",
    "Sector Strategies",
    "Technical Design",
    "Institutional Capacity",
    "Fiduciary",
    "Environment & Social",
    "Stakeholders"
  ),
  likelihood = c(1.88, 2.12, 3.00, 1.84, 2.16, 1.92, 2.08, 2.00),
  impact = c(3.02, 3.02, 4.00, 3.12, 3.12, 2.94, 2.94, 2.00),
  label = c(
    "Political & Governance",
    "Macroeconomic",
    "Sector Strategies",
    "Technical Design",
    "Institutional Capacity",
    "Fiduciary",
    "Environment & Social",
    "Stakeholders"
  ),
  color = c("#5DADE2", "#5DADE2", "#EC7063", "#F5B041", "#F5B041", "#F5B041", "#F5B041", "#7FB3D5"),
  textpos = c("top left", "top right", "top center", "middle left", "middle right", "bottom left", "bottom right", "top center"),
  stringsAsFactors = FALSE
)

# ------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------

ui <- page_navbar(
  title = "Azerbaijan WBG Operations Dashboard (FY25-29)",
  theme = bs_theme(version = 5, bootswatch = "flatly"),
  
  header = tags$head(
    tags$style(HTML("
      .navbar { font-weight: 600; }
      .card-header { font-weight: 700; }
      .small-muted { font-size: 12px; color: #6c757d; }
      .stage-box {
        border-radius: 10px;
        padding: 14px;
        color: white;
        min-height: 170px;
      }
      .metric-box {
        min-height: 150px !important;
      }
      .metric-box .bslib-value-box-value,
      .metric-box .value-box-value {
        font-size: clamp(2.2rem, 3.4vw, 4rem) !important;
        line-height: 1.02 !important;
        white-space: nowrap !important;
        overflow: visible !important;
      }
      .metric-box .bslib-value-box-title,
      .metric-box .value-box-title {
        font-size: 1.05rem !important;
        line-height: 1.2 !important;
        white-space: normal !important;
        overflow: visible !important;
      }
      .metric-box .bslib-value-box-showcase,
      .metric-box .value-box-showcase {
        font-size: 0.95rem !important;
        line-height: 1.1 !important;
        white-space: nowrap !important;
      }
      .metric-box .card-body,
      .metric-box .bslib-value-box,
      .metric-box .value-box-grid,
      .metric-box .bslib-fill {
        overflow: visible !important;
      }
      .table-sm td, .table-sm th { font-size: 13px; }
    "))
  ),
  
  sidebar = sidebar(
    width = 300,
    h5("CPF Reference"),
    div(class = "small-muted",
        strong("Country Partnership Framework"), tags$br(),
        "FY25-29 | Report No. 195625-AZ", tags$br(),
        "December 17, 2024 | IBRD + IFC + MIGA", tags$br(), tags$br(),
        strong("CBRA Statistical Bulletin"), tags$br(),
        "January 2026 (No. 310)"
    ),
    hr(),
    selectInput("kpi_category", "Filter KPI block", choices = c("All", unique(kpi_df$category)), selected = "All"),
    selectInput("pipeline_institution", "Filter institution", choices = c("All", unique(pipeline_df$institution)), selected = "All"),
    hr(),
    div(class = "small-muted",
        strong("Context"), tags$br(),
        "This dashboard combines CPF strategy, World Bank project-cycle framing, and Azerbaijan macro-financial monitoring.",
        tags$br(), tags$br(),
        "Top metric cards and the risk heatmap have been adjusted to improve readability."
    )
  ),
  
  nav_panel(
    "Executive Summary",
    layout_columns(
      col_widths = c(3, 3, 3, 3),
      value_box(title = "IBRD envelope", value = "US$1.0–1.5B", showcase = "FY25-29", class = "metric-box", theme = value_box_theme(bg = "#1B4F72", fg = "white")),
      value_box(title = "IFC expansion", value = "US$200–500M", showcase = "CPF period", class = "metric-box", theme = value_box_theme(bg = "#1ABC9C", fg = "white")),
      value_box(title = "CBAR reserves", value = "US$11.8B", showcase = "5.7 months of imports", class = "metric-box", theme = value_box_theme(bg = "#F39C12", fg = "white")),
      value_box(title = "NPL ratio", value = "2.6%", showcase = "Jan 2026", class = "metric-box", theme = value_box_theme(bg = "#E74C3C", fg = "white"))
    ),
    layout_columns(
      col_widths = c(8, 4),
      card(
        full_screen = TRUE,
        card_header("Strategic framing: challenges and two high-level outcomes"),
        card_body(
          layout_columns(
            col_widths = c(6, 6),
            div(style = "background:#EBF5FB; border-left:4px solid #1ABC9C; padding:14px; border-radius:6px;",
                h5(style = "color:#117A65;", "HLO 1: Increased Resilience & Sustainability"),
                tags$ul(
                  tags$li("Enhancing the shift to renewable energy"),
                  tags$li("Enhancing adaptation to climate change")
                ),
                p(class = "small-muted", "Energy transition, water, irrigation, climate adaptation, and sustainability-oriented resilience.")),
            div(style = "background:#FEF9E7; border-left:4px solid #E67E22; padding:14px; border-radius:6px;",
                h5(style = "color:#AF601A;", "HLO 2: Increased Productivity & Better Jobs"),
                tags$ul(
                  tags$li("Improving the business environment and access to employment"),
                  tags$li("Strengthening transport and digital connectivity")
                ),
                p(class = "small-muted", "Private sector growth, MSME finance, jobs, transport, and broadband connectivity."))
          )
        )
      ),
      card(full_screen = TRUE, card_header("Financial commitments mix"), card_body(plotlyOutput("finance_donut", height = "300px")))
    ),
    card(full_screen = TRUE, card_header("Development challenges"), card_body(DTOutput("challenges_table")))
  ),
  
  nav_panel(
    "WB Project Cycle",
    card(
      full_screen = TRUE,
      card_header("World Bank six-step project cycle and this dashboard's role"),
      card_body(
        layout_columns(
          col_widths = c(2, 2, 2, 2, 2, 2),
          div(class = "stage-box", style = "background:#1B4F72;", h5("1. Identification"), p("Country priorities and initial concept framing.")),
          div(class = "stage-box", style = "background:#1F618D;", h5("2. Preparation"), p("Technical, fiduciary, and institutional design.")),
          div(class = "stage-box", style = "background:#2874A6;", h5("3. Appraisal"), p("Feasibility, readiness, risk, and economic logic review.")),
          div(class = "stage-box", style = "background:#2E86C1;", h5("4. Negotiation / Approval"), p("Final documentation and approval process.")),
          div(class = "stage-box", style = "background:#3498DB;", h5("5. Implementation"), p("Execution, supervision, disbursement, and monitoring.")),
          div(class = "stage-box", style = "background:#5DADE2;", h5("6. Completion / Evaluation"), p("Results review, lessons, and validation."))
        )
      )
    ),
    layout_columns(
      col_widths = c(7, 5),
      card(full_screen = TRUE, card_header("Cycle stage relevance table"), card_body(DTOutput("cycle_table"))),
      card(full_screen = TRUE, card_header("How the dashboard supports the cycle"),
           card_body(tags$ul(
             tags$li(strong("Identification:"), " baseline diagnostics on oil dependence, private sector constraints, financial vulnerability, and human development context."),
             tags$li(strong("Preparation / Appraisal:"), " KPI structure, financing envelopes, and results-oriented monitoring views for CPF-style logic."),
             tags$li(strong("Implementation:"), " budget execution, bank loans, reserves, NPLs, and project pipeline monitoring."),
             tags$li(strong("Completion / Evaluation:"), " trend review and target-vs-baseline interpretation for retrospective evidence.")
           )))
    )
  ),
  
  nav_panel(
    "CPF KPI Tracker",
    layout_columns(
      col_widths = c(6, 6),
      card(full_screen = TRUE, card_header("KPI targets vs current values"), card_body(plotlyOutput("kpi_bar", height = "420px"))),
      card(
        full_screen = TRUE,
        card_header("Selected KPI notes"),
        card_body(tags$table(class = "table table-striped table-sm",
                             tags$thead(tags$tr(tags$th("Indicator"), tags$th("Target year"), tags$th("Note"))),
                             tags$tbody(lapply(seq_len(nrow(kpi_df)), function(i) {
                               tags$tr(tags$td(kpi_df$indicator[i]), tags$td(kpi_df$target_year[i]), tags$td(kpi_df$note[i]))
                             }))
        ))
      )
    ),
    card(full_screen = TRUE, card_header("Detailed KPI table"), card_body(DTOutput("kpi_table")))
  ),
  
  nav_panel(
    "Project Pipeline",
    layout_columns(
      col_widths = c(3, 3, 3, 3),
      value_box(title = "IBRD FY25-26 projects", value = "4", showcase = "Pipeline items", class = "metric-box", theme = value_box_theme(bg = "#1B4F72", fg = "white")),
      value_box(title = "Largest single project", value = "US$400M", showcase = "Agriculture & Irrigation", class = "metric-box", theme = value_box_theme(bg = "#1ABC9C", fg = "white")),
      value_box(title = "Current IFC portfolio", value = "US$47M", showcase = "Access Bank + Bank Respublika", class = "metric-box", theme = value_box_theme(bg = "#F39C12", fg = "white")),
      value_box(title = "Undisbursed IBRD", value = "US$176.1M", showcase = "Dec 2024", class = "metric-box", theme = value_box_theme(bg = "#9B59B6", fg = "white"))
    ),
    layout_columns(
      col_widths = c(6, 6),
      card(full_screen = TRUE, card_header("Pipeline by stage"), card_body(plotlyOutput("pipeline_stage_plot", height = "320px"))),
      card(full_screen = TRUE, card_header("Pipeline by institution / focus"), card_body(plotlyOutput("pipeline_focus_plot", height = "320px")))
    ),
    card(full_screen = TRUE, card_header("Pipeline detail table"), card_body(DTOutput("pipeline_table")))
  ),
  
  nav_panel(
    "Financial Sector",
    layout_columns(
      col_widths = c(3, 3, 2, 4),
      value_box(title = "Total Bank Assets (Jan 2026)", value = "56,936", showcase = "mln AZN", class = "metric-box", theme = value_box_theme(bg = "#1B4F72", fg = "white")),
      value_box(title = "Total Loans (Jan 2026)", value = "29,980", showcase = "mln AZN", class = "metric-box", theme = value_box_theme(bg = "#1ABC9C", fg = "white")),
      value_box(title = "NPL Ratio (Jan 2026)", value = "2.6%", showcase = "banking sector", class = "metric-box", theme = value_box_theme(bg = "#F39C12", fg = "white")),
      value_box(title = "Net Profit 2025", value = "1,162", showcase = "mln AZN", class = "metric-box", theme = value_box_theme(bg = "#9B59B6", fg = "white"))
    ),
    layout_columns(
      col_widths = c(8, 4),
      card(full_screen = TRUE, card_header("Loan trend by bank type"), card_body(plotlyOutput("loan_trend_plot", height = "300px"))),
      card(full_screen = TRUE, card_header("NPL ratio reference"),
           card_body(plotlyOutput("npl_ref_plot", height = "300px")))
    ),
    layout_columns(
      col_widths = c(6, 6),
      card(full_screen = TRUE, card_header("Sectoral loan breakdown (Jan 2026)"), card_body(plotlyOutput("sector_pie_plot", height = "320px"))),
      card(full_screen = TRUE, card_header("Macro / financial snapshot"), card_body(DTOutput("macro_cards_table")))
    )
  ),
  
  nav_panel(
    "Macroeconomics",
    layout_columns(
      col_widths = c(3, 3, 3, 3),
      value_box(title = "GDP Growth 2025", value = "1.4%", showcase = "Non-oil: 2.7%", class = "metric-box", theme = value_box_theme(bg = "#1B4F72", fg = "white")),
      value_box(title = "CPI 12-month (Jan 2026)", value = "5.7%", showcase = "Target: 4±2%", class = "metric-box", theme = value_box_theme(bg = "#F39C12", fg = "white")),
      value_box(title = "Budget Balance 2025", value = "+0.4% GDP", showcase = "Surplus 528 mln AZN", class = "metric-box", theme = value_box_theme(bg = "#1ABC9C", fg = "white")),
      value_box(title = "Avg Monthly Wage 2025", value = "1,103 AZN", showcase = "+9.3% YoY", class = "metric-box", theme = value_box_theme(bg = "#9B59B6", fg = "white"))
    ),
    layout_columns(
      col_widths = c(6, 6),
      card(full_screen = TRUE, card_header("Budget execution: 2025 full year vs Jan 2026"), card_body(plotlyOutput("budget_plot", height = "320px"))),
      card(full_screen = TRUE, card_header("Selected macro forecasts"), card_body(DTOutput("macro_forecast_table")))
    )
  ),
  
  nav_panel(
    "Risk Register",
    layout_columns(
      col_widths = c(5, 7),
      card(full_screen = TRUE, card_header("CPF Risk Rating Matrix (FY25-29)"), card_body(DTOutput("risk_table"))),
      card(full_screen = TRUE, card_header("Risk Likelihood × Impact Heatmap"), card_body(plotlyOutput("risk_heatmap", height = "420px")))
    ),
    card(
      full_screen = TRUE,
      card_header("Key Risk Mitigation Strategies"),
      card_body(
        layout_columns(
          col_widths = c(4, 4, 4),
          div(h6("Political & Governance (Moderate)"), p("Maintain close dialogue with government; flexible program design; shift engagement to sectors with traction if progress stalls.")),
          div(h6("Sector Strategies (Substantial — highest risk)"), p("Assess institutional and regulatory environment before launching operations. Build commercial readiness before scaling investment.")),
          div(h6("Macroeconomic (Moderate)"), p("Use reserve and fiscal buffers as context, while monitoring oil-related volatility, growth, and external balances."))
        )
      )
    )
  )
)

# ------------------------------------------------------------------------------
# SERVER
# ------------------------------------------------------------------------------

server <- function(input, output, session) {
  
  filtered_kpi <- reactive({
    if (input$kpi_category == "All") return(kpi_df)
    dplyr::filter(kpi_df, category == input$kpi_category)
  })
  
  filtered_pipeline <- reactive({
    if (input$pipeline_institution == "All") return(pipeline_df)
    dplyr::filter(pipeline_df, institution == input$pipeline_institution)
  })
  
  output$finance_donut <- renderPlotly({
    plot_ly(financial_commitments_df, labels = ~category, values = ~amount, type = "pie", hole = 0.55,
            textinfo = "label+percent") %>%
      layout(showlegend = FALSE)
  })
  
  output$challenges_table <- renderDT({
    datatable(challenges_df, rownames = FALSE,
              options = list(pageLength = 10, dom = "tip", scrollX = TRUE))
  })
  
  output$cycle_table <- renderDT({
    datatable(cycle_df, rownames = FALSE,
              options = list(pageLength = 6, dom = "tip", scrollX = TRUE),
              colnames = c("Stage", "What happens", "How this repository / dashboard supports it"))
  })
  
  output$kpi_bar <- renderPlotly({
    df <- filtered_kpi()
    plot_ly(df, x = ~indicator, y = ~target, type = "bar", name = "Target", marker = list(color = "#1B4F72")) %>%
      add_trace(y = ~current, name = "Current", marker = list(color = "#1ABC9C")) %>%
      layout(barmode = "group", xaxis = list(title = "", tickangle = -35), yaxis = list(title = "Value"),
             legend = list(orientation = "h", x = 0.2, y = 1.15))
  })
  
  output$kpi_table <- renderDT({
    df <- filtered_kpi() %>%
      mutate(
        baseline_display = ifelse(is.na(baseline), "—", paste0(comma(baseline), " ", unit)),
        current_display = ifelse(is.na(current), "—", paste0(comma(current), " ", unit)),
        target_display = ifelse(is.na(target), "—", paste0(comma(target), " ", unit)),
        progress_display = ifelse(is.na(progress_pct), "N/A", paste0(round(progress_pct, 1), "%"))
      ) %>%
      select(category, indicator, baseline_display, current_display, target_display, target_year, progress_display, note)
    
    datatable(df, rownames = FALSE,
              options = list(pageLength = 15, scrollX = TRUE),
              colnames = c("Block", "Indicator", "Baseline", "Current", "Target", "Target year", "Progress", "Note"))
  })
  
  output$pipeline_stage_plot <- renderPlotly({
    df <- filtered_pipeline() %>% group_by(stage) %>% summarise(amount_usd_m = sum(amount_usd_m), .groups = "drop")
    plot_ly(df, x = ~stage, y = ~amount_usd_m, type = "bar", marker = list(color = "#2874A6")) %>%
      layout(yaxis = list(title = "USD million"), xaxis = list(title = ""))
  })
  
  output$pipeline_focus_plot <- renderPlotly({
    df <- filtered_pipeline()
    plot_ly(df, x = ~focus, y = ~amount_usd_m, color = ~institution, type = "bar") %>%
      layout(barmode = "group", yaxis = list(title = "USD million"), xaxis = list(title = "", tickangle = -20))
  })
  
  output$pipeline_table <- renderDT({
    datatable(filtered_pipeline(), rownames = FALSE,
              options = list(pageLength = 10, scrollX = TRUE))
  })
  
  output$budget_plot <- renderPlotly({
    plot_ly(budget_df, x = ~indicator, y = ~full_year_2025, type = "bar", name = "2025 Full Year", marker = list(color = "#1B4F72")) %>%
      add_trace(y = ~jan_2026, name = "Jan 2026", marker = list(color = "#1ABC9C")) %>%
      layout(barmode = "group", yaxis = list(title = "mln AZN"), xaxis = list(title = ""))
  })
  
  output$macro_cards_table <- renderDT({
    datatable(macro_cards_df, rownames = FALSE,
              options = list(pageLength = 10, dom = "tip", scrollX = TRUE),
              colnames = c("Metric", "Value", "Note"))
  })
  
  output$loan_trend_plot <- renderPlotly({
    plot_ly(loan_trend_df, x = ~period, y = ~total_loans, type = "scatter", mode = "lines+markers", name = "Total loans", line = list(color = "#1B4F72")) %>%
      add_trace(y = ~private_banks, name = "Private banks", line = list(color = "#1ABC9C")) %>%
      add_trace(y = ~state_owned_banks, name = "State-owned banks", line = list(color = "#F39C12")) %>%
      layout(yaxis = list(title = "mln AZN"), xaxis = list(title = ""))
  })
  
  output$npl_ref_plot <- renderPlotly({
    npl_df <- data.frame(period = c("Target / reference", "Actual Jan 2026"), value = c(3.0, 2.6))
    plot_ly(npl_df, x = ~period, y = ~value, type = "bar", marker = list(color = c("#FAD7A0", "#E67E22"))) %>%
      layout(yaxis = list(title = "%"), xaxis = list(title = ""))
  })
  
  output$sector_pie_plot <- renderPlotly({
    plot_ly(sector_df, labels = ~sector, values = ~balance, type = "pie", hole = 0.45, textinfo = "label+percent") %>%
      layout(showlegend = FALSE)
  })
  
  output$macro_forecast_table <- renderDT({
    datatable(macro_forecast_df, rownames = FALSE,
              options = list(dom = "tip", pageLength = 10, scrollX = TRUE))
  })
  
  output$risk_table <- renderDT({
    datatable(risk_df, rownames = FALSE,
              options = list(dom = "tip", pageLength = 10),
              colnames = c("Risk Category", "Rating", "Meaning")) %>%
      formatStyle("rating", backgroundColor = styleEqual(c("M", "S"), c("#E8E3D3", "#F3E1C6")))
  })
  
  output$risk_heatmap <- renderPlotly({
    bg_shapes <- list(
      list(type = "rect", x0 = 0.5, x1 = 2.5, y0 = 0.5, y1 = 2.5, fillcolor = "#EAF2F8", line = list(width = 0), layer = "below"),
      list(type = "rect", x0 = 2.5, x1 = 4.5, y0 = 0.5, y1 = 2.5, fillcolor = "#FCF3CF", line = list(width = 0), layer = "below"),
      list(type = "rect", x0 = 0.5, x1 = 2.5, y0 = 2.5, y1 = 4.5, fillcolor = "#FDEDEC", line = list(width = 0), layer = "below"),
      list(type = "rect", x0 = 2.5, x1 = 4.5, y0 = 2.5, y1 = 4.5, fillcolor = "#FDF2E9", line = list(width = 0), layer = "below")
    )
    
    plot_ly() %>%
      add_trace(
        data = risk_points,
        x = ~likelihood,
        y = ~impact,
        type = "scatter",
        mode = "markers+text",
        text = ~label,
        textposition = risk_points$textpos,
        textfont = list(size = 11),
        marker = list(size = 18, color = risk_points$color, line = list(width = 1, color = "white")),
        hovertemplate = paste0("<b>%{text}</b><br>", "Likelihood: %{x}<br>", "Impact: %{y}<br><extra></extra>"),
        cliponaxis = FALSE
      ) %>%
      layout(
        xaxis = list(title = "Likelihood (1 = Low, 4 = High)", range = c(0.5, 4.5), dtick = 1, zeroline = FALSE),
        yaxis = list(title = "Impact (1 = Low, 4 = High)", range = c(0.5, 4.5), dtick = 1, zeroline = FALSE),
        shapes = bg_shapes,
        margin = list(t = 20, r = 90, b = 70, l = 90)
      )
  })
}

shinyApp(ui, server)
