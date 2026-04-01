# app.R
# Azerbaijan CPF Analysis Shiny App (completed diversification charts)

library(shiny)
library(bslib)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)
library(readr)
library(scales)
library(DT)
library(plotly)
library(stringr)

safe_read_csv <- function(path) {
  if (!file.exists(path)) return(NULL)
  readr::read_csv(path, show_col_types = FALSE)
}

normalize_period_type <- function(x) {
  x <- tolower(trimws(as.character(x)))
  dplyr::case_when(
    x %in% c("annual", "year", "yearly") ~ "annual",
    x %in% c("quarter", "quarterly", "q") ~ "quarterly",
    x %in% c("month", "monthly", "m") ~ "monthly",
    TRUE ~ x
  )
}

parse_period_date <- function(x) suppressWarnings(as.Date(x))

convert_prev100_to_yoy <- function(x) {
  x_num <- suppressWarnings(as.numeric(x))
  dplyr::if_else(!is.na(x_num) & x_num > 80 & x_num < 130, x_num - 100, x_num)
}

prep_periodic <- function(df) {
  if (is.null(df)) return(NULL)
  out <- df %>%
    mutate(
      period_date = parse_period_date(period_date),
      period_type = normalize_period_type(period_type)
    ) %>%
    arrange(period_date)

  if ("real_gdp_growth_pct" %in% names(out)) {
    out <- out %>% mutate(real_gdp_growth_yoy_pct = convert_prev100_to_yoy(real_gdp_growth_pct))
  }
  if ("non_oil_gdp_growth_pct" %in% names(out)) {
    out <- out %>% mutate(non_oil_gdp_growth_yoy_pct = convert_prev100_to_yoy(non_oil_gdp_growth_pct))
  }
  out
}

latest_non_null <- function(df, value_col, period_filter = NULL) {
  if (is.null(df) || !(value_col %in% names(df))) return(NA_real_)
  tmp <- df
  if (!is.null(period_filter) && "period_type" %in% names(tmp)) {
    tmp <- tmp %>% filter(period_type %in% period_filter)
  }
  tmp <- tmp %>% filter(!is.na(.data[[value_col]])) %>% arrange(period_date)
  if (nrow(tmp) == 0) return(NA_real_)
  tail(tmp[[value_col]], 1)
}

metric_box <- function(title, value, showcase = NULL) {
  value_box(
    title = title,
    value = value,
    showcase = showcase,
    theme = value_box_theme(bg = "#f8fafc", fg = "#111827")
  )
}

percent_or_na <- function(x, accuracy = 0.1) {
  ifelse(is.na(x), "N/A", scales::number(x, accuracy = accuracy, suffix = "%"))
}

number_or_na <- function(x, accuracy = 0.1, suffix = "") {
  ifelse(is.na(x), "N/A", scales::number(x, accuracy = accuracy, big.mark = ",", suffix = suffix))
}

pick_first_existing <- function(df, candidates) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) return(NULL)
  hit[[1]]
}

build_benchmark <- function(gdp_latest, wgi_latest, findex_latest) {
  if (is.null(gdp_latest) && is.null(wgi_latest) && is.null(findex_latest)) return(NULL)

  out <- tibble(country_iso = character(), country_name = character())

  if (!is.null(gdp_latest) && all(c("country_iso", "country_name", "value") %in% names(gdp_latest))) {
    out <- full_join(
      out,
      gdp_latest %>% transmute(country_iso, country_name, gdp_per_capita = as.numeric(value)),
      by = c("country_iso", "country_name")
    )
  } else if (!is.null(gdp_latest) && all(c("country_iso", "country_name", "gdp_per_capita") %in% names(gdp_latest))) {
    out <- full_join(
      out,
      gdp_latest %>% transmute(country_iso, country_name, gdp_per_capita = as.numeric(gdp_per_capita)),
      by = c("country_iso", "country_name")
    )
  }

  if (!is.null(wgi_latest) && all(c("country_iso", "country_name") %in% names(wgi_latest))) {
    wgi_cols <- intersect(c("government_effectiveness", "regulatory_quality", "rule_of_law", "control_of_corruption"), names(wgi_latest))
    if (length(wgi_cols) > 0) {
      out <- full_join(
        out,
        wgi_latest %>%
          mutate(institutions_avg = rowMeans(across(all_of(wgi_cols)), na.rm = TRUE)) %>%
          transmute(country_iso, country_name, institutions_avg),
        by = c("country_iso", "country_name")
      )
    }
  }

  if (!is.null(findex_latest) && all(c("country_iso", "country_name") %in% names(findex_latest))) {
    fin_cols <- intersect(c("account_ownership_pct", "digital_payment_pct", "mobile_money_account_pct"), names(findex_latest))
    if (length(fin_cols) > 0) {
      out <- full_join(
        out,
        findex_latest %>%
          mutate(financial_inclusion_avg = rowMeans(across(all_of(fin_cols)), na.rm = TRUE)) %>%
          transmute(country_iso, country_name, financial_inclusion_avg),
        by = c("country_iso", "country_name")
      )
    }
  }

  out
}

ui <- page_navbar(
  title = "Azerbaijan CPF Analysis Dashboard (Jan-2026)",
  theme = bs_theme(version = 5, bootswatch = "flatly"),
  sidebar = sidebar(
    width = 320,
    h4("Data inputs"),
    div(style = "margin-bottom:12px;", strong("Azerbaijan Credit Access and Stability (Gold)"), br(), code("outputs/tables/aze_credit_access_and_stability_periodic.csv")),
    div(style = "margin-bottom:12px;", strong("Azerbaijan Digital Finance (Gold)"), br(), code("outputs/tables/aze_digital_finance_periodic.csv")),
    div(style = "margin-bottom:12px;", strong("Azerbaijan Economic Diversification (Gold)"), br(), code("outputs/tables/aze_economic_diversification_periodic.csv")),
    hr(),
    h5("Optional World Bank benchmark files"),
    div(style = "margin-bottom:12px;", strong("World Bank GDP per capita (latest)"), br(), code("outputs/tables/gdp_per_capita_country_latest.csv")),
    div(style = "margin-bottom:12px;", strong("Worldwide Governance Indicators (latest)"), br(), code("outputs/tables/wgi_country_latest.csv")),
    div(style = "margin-bottom:12px;", strong("Global Findex (latest)"), br(), code("outputs/tables/global_findex_country_latest.csv")),
    hr(),
    sliderInput("year_window", "Visible date window", min = 2022, max = year(Sys.Date()), value = c(2022, year(Sys.Date())), sep = ""),
    actionButton("reload", "Reload data", class = "btn-primary")
  ),
  nav_panel(
    "Executive Summary",
    layout_columns(col_widths = c(4, 4, 4), uiOutput("vb_non_oil_growth"), uiOutput("vb_inflation"), uiOutput("vb_mobile_banking")),
    layout_columns(col_widths = c(4, 4, 4), uiOutput("vb_npl"), uiOutput("vb_ecommerce"), uiOutput("vb_non_oil_export_share")),
    card(full_screen = TRUE, card_header("CPF lens: from Easterly's incentives framework to Azerbaijan monitoring"), card_body(htmlOutput("executive_text"))),
    layout_columns(
      card(full_screen = TRUE, card_header("Macro stability and diversification"), plotlyOutput("summary_macro_plot", height = 320)),
      card(full_screen = TRUE, card_header("Digital finance adoption"), plotlyOutput("summary_digital_plot", height = 320))
    )
  ),
  nav_panel(
    "1. Incentives & Stability",
    layout_columns(
      card(full_screen = TRUE, card_header("Growth, inflation, and lending conditions"), plotlyOutput("stability_plot", height = 380)),
      card(full_screen = TRUE, card_header("NPL ratio vs lending rates"), plotlyOutput("npl_rate_plot", height = 380))
    ),
    layout_columns(
      card(full_screen = TRUE, card_header("Business lending by firm size"), plotlyOutput("msme_plot", height = 360)),
      card(full_screen = TRUE, card_header("Annual Loan allocation by sector: 2025"), plotlyOutput("sector_plot", height = 360))
    ),
    card(full_screen = TRUE, card_header("Financial stability data table"), DTOutput("credit_table"))
  ),
  nav_panel(
    "2. Digital Finance",
    layout_columns(
      card(full_screen = TRUE, card_header("POS infrastructure rollout"), plotlyOutput("infra_plot", height = 360)),
      card(full_screen = TRUE, card_header("Cashless usage and e-commerce"), plotlyOutput("cashless_plot", height = 360))
    ),
    layout_columns(
      card(full_screen = TRUE, card_header("Instant / national payment system usage (IPS & LVPCSS)"), plotlyOutput("nps_plot", height = 360)),
      card(full_screen = TRUE, card_header("Mobile and internet banking adoption"), plotlyOutput("ebanking_plot", height = 360))
    ),
    card(full_screen = TRUE, card_header("Digital finance data table"), DTOutput("digital_table"))
  ),
  nav_panel(
    "3. Diversification",
    layout_columns(
      card(full_screen = TRUE, card_header("Real GDP vs non-oil GDP growth"), plotlyOutput("growth_plot", height = 360)),
      card(full_screen = TRUE, card_header("Trade structure: oil/gas vs other exports"), plotlyOutput("trade_structure_plot", height = 360))
    ),
    layout_columns(
      card(full_screen = TRUE, card_header("Current account and trade balance"), plotlyOutput("external_balance_plot", height = 360)),
      card(full_screen = TRUE, card_header("Investment and wage dynamics (y/y)"), plotlyOutput("income_plot", height = 360))
    ),
    card(full_screen = TRUE, card_header("Economic diversification data table"), DTOutput("div_table"))
  ),
  nav_panel(
    "4. Benchmark & Narrative",
    card(
      full_screen = TRUE,
      card_header("Suggested CPF storylines"),
      htmlOutput("storyline_text")
    ),
    card(
      full_screen = TRUE,
      card_header("Benchmark table"),
      DTOutput("benchmark_table")
    )
  )
)

server <- function(input, output, session) {
  data_bundle <- eventReactive(input$reload, {
    credit <- prep_periodic(safe_read_csv("outputs/tables/aze_credit_access_and_stability_periodic.csv"))
    digital <- prep_periodic(safe_read_csv("outputs/tables/aze_digital_finance_periodic.csv"))
    diversification <- prep_periodic(safe_read_csv("outputs/tables/aze_economic_diversification_periodic.csv"))

    gdp_latest <- safe_read_csv("outputs/tables/gdp_per_capita_country_latest.csv")
    wgi_latest <- safe_read_csv("outputs/tables/wgi_country_latest.csv")
    findex_latest <- safe_read_csv("outputs/tables/global_findex_country_latest.csv")

    list(
      credit = credit,
      digital = digital,
      diversification = diversification,
      benchmark = build_benchmark(gdp_latest, wgi_latest, findex_latest)
    )
  }, ignoreNULL = FALSE)

  filtered_credit <- reactive({
    df <- data_bundle()$credit
    if (is.null(df)) return(NULL)
    df %>% filter(year(period_date) >= input$year_window[1], year(period_date) <= input$year_window[2])
  })
  filtered_digital <- reactive({
    df <- data_bundle()$digital
    if (is.null(df)) return(NULL)
    df %>% filter(year(period_date) >= input$year_window[1], year(period_date) <= input$year_window[2])
  })
  filtered_div <- reactive({
    df <- data_bundle()$diversification
    if (is.null(df)) return(NULL)
    df %>% filter(year(period_date) >= input$year_window[1], year(period_date) <= input$year_window[2])
  })

  output$vb_non_oil_growth <- renderUI({
    df <- filtered_div()
    x <- latest_non_null(df, "non_oil_gdp_growth_yoy_pct", c("annual", "monthly"))
    index_basis <- latest_non_null(df, "non_oil_gdp_growth_pct", c("annual", "monthly"))
    if (is.na(index_basis)) index_basis <- latest_non_null(df, "non_oil_gdp_growth_pct", c("annual", "monthly"))
    subtitle_txt <- NULL
    if (!is.na(index_basis) && index_basis > 80 && index_basis < 130) {
      subtitle_txt <- paste0("CBAR index basis: ", scales::number(index_basis, accuracy = 0.1), " (previous year = 100)")
    }
    metric_box("Latest non-oil GDP growth (y/y)", percent_or_na(x),
               showcase = if (!is.null(subtitle_txt)) span(style = "font-size: 0.8rem;", subtitle_txt) else NULL)
  })
  output$vb_inflation <- renderUI({
    metric_box("Latest CPI (12m)", percent_or_na(latest_non_null(filtered_div(), "cpi_12m_pct", c("monthly", "annual"))))
  })
  output$vb_mobile_banking <- renderUI({
    metric_box("Latest mobile banking users", number_or_na(latest_non_null(filtered_digital(), "mobile_banking_users_count", c("monthly")), accuracy = 1))
  })
  output$vb_npl <- renderUI({
    df <- filtered_credit()
    x <- latest_non_null(df, "loan_avg_rate_azn_pct", c("monthly", "quarterly", "annual"))
    title <- "Latest loan avg rate"
    if (is.na(x)) x <- latest_non_null(df, "avg_loan_rate_pct", c("monthly", "quarterly", "annual"))
    if (is.na(x)) {
      x <- latest_non_null(df, "avg_business_loan_rate_pct", c("monthly", "quarterly", "annual"))
      title <- "Latest business loan rate"
    }
    if (is.na(x)) {
      x <- latest_non_null(df, "npl_ratio_pct", c("monthly", "quarterly", "annual"))
      title <- "Latest NPL ratio"
    }
    metric_box(title, percent_or_na(x))
  })
  output$vb_ecommerce <- renderUI({
    metric_box("Latest e-commerce amount", number_or_na(latest_non_null(filtered_digital(), "ecommerce_amount_mn_azn", c("monthly")), accuracy = 0.1, suffix = " mn AZN"))
  })
  output$vb_non_oil_export_share <- renderUI({
    df <- filtered_div()
    num_col <- pick_first_existing(df, c("other_exports_mn_usd", "non_oil_exports_mn_usd"))
    den_col <- pick_first_existing(df, c("goods_exports_total_mn_usd", "total_exports_mn_usd"))
    val <- NA_real_
    if (!is.null(num_col) && !is.null(den_col)) {
      tmp <- df %>%
        filter(!is.na(.data[[num_col]]), !is.na(.data[[den_col]]), .data[[den_col]] > 0) %>%
        mutate(non_oil_export_share = 100 * .data[[num_col]] / .data[[den_col]]) %>%
        arrange(period_date)
      if (nrow(tmp) > 0) val <- tail(tmp$non_oil_export_share, 1)
    }
    metric_box("Latest non-oil export share", percent_or_na(val))
  })

  output$executive_text <- renderText({
    paste0(
      "<p><b>Easterly's lens</b> is useful here because it shifts attention away from single panaceas and toward the incentives that sustain growth: macro stability, credible finance, productive investment, and institutions that reward innovation rather than rent-seeking.</p>",
      "<ul>",
      "<li><b>Incentives and stability:</b> real growth, inflation, NPL ratios, and lending rates help show whether firms face a predictable environment for long-term investment.</li>",
      "<li><b>Digital finance:</b> POS rollout, card usage, IPS transactions, and mobile banking track whether transaction costs are falling and whether firms and households can participate more easily in the formal economy.</li>",
      "<li><b>Diversification:</b> derived non-oil GDP growth (from CBAR previous-year=100 index), other exports, and current-account structure help assess whether growth is broadening beyond hydrocarbons.</li>",
      "</ul>"
    )
  })

  output$summary_macro_plot <- renderPlotly({
    df <- filtered_div(); req(df)
    plot_df <- df %>% filter(period_type %in% c("annual", "monthly")) %>%
      select(period_date, real_gdp_growth_yoy_pct, non_oil_gdp_growth_yoy_pct, cpi_12m_pct) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = metric)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "%", color = NULL) +
      theme_minimal(base_size = 13) +
      scale_color_discrete(labels = c(
        cpi_12m_pct = "CPI (12m)",
        non_oil_gdp_growth_yoy_pct = "Non-oil GDP growth (y/y)",
        real_gdp_growth_yoy_pct = "Real GDP growth (y/y)"
      ))
    ggplotly(p)
  })

  output$summary_digital_plot <- renderPlotly({
    df <- filtered_digital(); req(df)
    plot_df <- df %>%
      filter(period_type == "monthly") %>%
      select(period_date, contactless_pos_total_units, mobile_banking_users_count, ecommerce_amount_mn_azn) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = metric)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = NULL, color = NULL) +
      theme_minimal(base_size = 13) +
      scale_color_discrete(labels = c(
        contactless_pos_total_units = "Contactless POS",
        ecommerce_amount_mn_azn = "E-commerce amount",
        mobile_banking_users_count = "Mobile banking users"
      ))
    ggplotly(p)
  })

  output$stability_plot <- renderPlotly({
    df1 <- filtered_div(); df2 <- filtered_credit(); req(df1, df2)
    p <- ggplot() +
      geom_line(data = df1 %>% filter(period_type %in% c("annual", "monthly")),
                aes(period_date, real_gdp_growth_yoy_pct, color = "Real GDP growth (y/y)"), linewidth = 1, na.rm = TRUE) +
      geom_line(data = df1 %>% filter(period_type %in% c("annual", "monthly")),
                aes(period_date, cpi_12m_pct, color = "CPI (12m)"), linewidth = 1, na.rm = TRUE) +
      geom_line(data = df2,
                aes(period_date, loan_avg_rate_azn_pct, color = "Average AZN loan rate"), linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "%", color = NULL) +
      theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$npl_rate_plot <- renderPlotly({
    df <- filtered_credit(); req(df)
    p <- ggplot(df, aes(period_date)) +
      geom_line(aes(y = npl_ratio_pct, color = "NPL ratio"), linewidth = 1, na.rm = TRUE) +
      geom_line(aes(y = loan_avg_rate_azn_pct, color = "AZN loan rate"), linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "%", color = NULL) +
      theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$msme_plot <- renderPlotly({
    df <- filtered_credit(); req(df)
    plot_df <- df %>%
      select(period_date, micro_business_loans_mn_azn, small_business_loans_mn_azn,
             medium_business_loans_mn_azn, large_business_loans_mn_azn) %>%
      pivot_longer(-period_date, names_to = "size", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = size)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "mn AZN", color = NULL) +
      theme_minimal(base_size = 13) +
      scale_color_discrete(labels = c(
        large_business_loans_mn_azn = "Large",
        medium_business_loans_mn_azn = "Medium",
        micro_business_loans_mn_azn = "Micro",
        small_business_loans_mn_azn = "Small"
      ))
    ggplotly(p)
  })
  output$sector_plot <- renderPlotly({
    df <- filtered_credit(); req(df)
    sector_cols <- c("agriculture_loans_mn_azn", "construction_loans_mn_azn", "industry_manufacturing_loans_mn_azn",
                     "trade_and_services_loans_mn_azn", "transport_communication_loans_mn_azn", "households_loans_mn_azn")
    req(all(c("period_date", "period_type", sector_cols) %in% names(df)))
    annual_df <- df %>% filter(period_type == "annual") %>% filter(!if_all(all_of(sector_cols), is.na)) %>% arrange(period_date)
    req(nrow(annual_df) >= 1)
    latest_annual <- slice_tail(annual_df, n = 1)
    latest_year <- lubridate::year(latest_annual$period_date)
    plot_df <- latest_annual %>% select(all_of(sector_cols)) %>% pivot_longer(everything(), names_to = "sector", values_to = "latest_value") %>%
      filter(!is.na(latest_value)) %>%
      mutate(
        sector_label = recode(
          sector,
          agriculture_loans_mn_azn = "Agriculture",
          construction_loans_mn_azn = "Construction",
          industry_manufacturing_loans_mn_azn = "Industry",
          trade_and_services_loans_mn_azn = "Trade & Services",
          transport_communication_loans_mn_azn = "Transport & Comms",
          households_loans_mn_azn = "Households"
        ),
        hover_text = paste0("Sector: ", sector_label, "<br>Year: ", latest_year, "<br>Value: ", scales::comma(round(latest_value, 1)), " mn AZN")
      ) %>% arrange(latest_value)
    p <- ggplot(plot_df, aes(latest_value, reorder(sector_label, latest_value), text = hover_text)) +
      geom_col() + labs(x = "mn AZN", y = NULL) + theme_minimal(base_size = 13)
    ggplotly(p, tooltip = "text")
  })
  output$credit_table <- renderDT({
    df <- filtered_credit(); req(df)
    datatable(df %>% arrange(desc(period_date)), extensions = "Buttons",
              options = list(dom = "Bfrtip", buttons = c("copy", "csv", "excel"), pageLength = 12, scrollX = TRUE))
  })

  output$infra_plot <- renderPlotly({
    df <- filtered_digital(); req(df)
    req(all(c("period_date", "period_type", "pos_total_units", "contactless_pos_total_units") %in% names(df)))
    plot_df <- df %>% filter(period_type == "monthly") %>%
      select(period_date, pos_total_units, contactless_pos_total_units) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value") %>%
      mutate(metric_label = recode(metric, pos_total_units = "Total POS", contactless_pos_total_units = "Contactless POS")) %>%
      filter(!is.na(value))
    p <- ggplot(plot_df, aes(period_date, value, color = metric_label)) +
      geom_line(linewidth = 1) + labs(x = NULL, y = "Units", color = NULL) + theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$cashless_plot <- renderPlotly({
    df <- filtered_digital(); req(df)
    plot_df <- df %>% filter(period_type == "monthly") %>%
      select(period_date, non_cash_pos_amount_mn_azn, ecommerce_amount_mn_azn, contactless_pos_amount_mn_azn) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = metric)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "mn AZN", color = NULL) +
      theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$nps_plot <- renderPlotly({
    df <- filtered_digital(); req(df)
    req(all(c("period_date", "ips_txn_amount_mn_azn", "lvpcss_txn_amount_mn_azn") %in% names(df)))
    plot_df <- df %>% select(period_date, ips_txn_amount_mn_azn, lvpcss_txn_amount_mn_azn) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = metric)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = "mn AZN", color = NULL) +
      theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$ebanking_plot <- renderPlotly({
    df <- filtered_digital(); req(df)
    plot_df <- df %>% filter(period_type == "monthly") %>%
      select(period_date, internet_banking_users_count, mobile_banking_users_count, payment_cards_contactless_thousand) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value")
    p <- ggplot(plot_df, aes(period_date, value, color = metric)) +
      geom_line(linewidth = 1, na.rm = TRUE) +
      labs(x = NULL, y = NULL, color = NULL) +
      theme_minimal(base_size = 13)
    ggplotly(p)
  })
  output$digital_table <- renderDT({
    df <- filtered_digital(); req(df)
    datatable(df %>% arrange(desc(period_date)), extensions = "Buttons",
              options = list(dom = "Bfrtip", buttons = c("copy", "csv", "excel"), pageLength = 12, scrollX = TRUE))
  })

  output$growth_plot <- renderPlotly({
    df <- filtered_div(); req(df)

    plot_df <- df %>%
      filter(period_type %in% c("annual", "monthly")) %>%
      select(period_date, real_gdp_growth_yoy_pct, non_oil_gdp_growth_yoy_pct) %>%
      pivot_longer(-period_date, names_to = "metric", values_to = "value") %>%
      filter(!is.na(value)) %>%
      mutate(
        metric_label = recode(
          metric,
          real_gdp_growth_yoy_pct = "Real GDP growth (y/y)",
          non_oil_gdp_growth_yoy_pct = "Non-oil GDP growth (y/y)"
        )
      )

    p <- ggplot(plot_df, aes(period_date, value, color = metric_label, group = metric_label)) +
      geom_line(linewidth = 1.1, na.rm = TRUE) +
      labs(x = NULL, y = "%", color = NULL) +
      theme_minimal(base_size = 13)

    ggplotly(p)
  })

  output$trade_structure_plot <- renderPlotly({
    df <- filtered_div(); req(df)
    oil_col <- pick_first_existing(df, c("oil_gas_exports_mn_usd", "oil_exports_mn_usd"))
    other_col <- pick_first_existing(df, c("other_exports_mn_usd", "non_oil_exports_mn_usd"))
    validate(need(!is.null(oil_col) || !is.null(other_col), "Trade structure columns not found."))

    cols <- c("period_date", "period_type", oil_col, other_col)
    cols <- cols[!duplicated(cols) & !is.na(cols)]

    plot_df <- df %>%
      filter(period_type == "quarterly") %>%
      select(all_of(cols)) %>%
      pivot_longer(cols = -c(period_date, period_type), names_to = "metric", values_to = "value") %>%
      mutate(value = suppressWarnings(as.numeric(value))) %>%
      filter(!is.na(value)) %>%
      arrange(metric, period_date) %>%
      mutate(
        metric_label = recode(metric,
          oil_gas_exports_mn_usd = "Oil & gas exports",
          oil_exports_mn_usd = "Oil & gas exports",
          other_exports_mn_usd = "Other exports",
          non_oil_exports_mn_usd = "Other exports"
        ),
        hover_text = paste0(
          "Quarter: ", format(period_date, "%Y-%m"),
          "<br>Metric: ", metric_label,
          "<br>Value: ", scales::comma(round(value, 1)), " mn USD"
        )
      )

    validate(need(nrow(plot_df) > 0, "No quarterly trade structure data available."))

    p <- ggplot(plot_df, aes(period_date, value, color = metric_label, group = metric_label, text = hover_text)) +
      geom_line(linewidth = 1.3, na.rm = TRUE) +
      geom_point(size = 2.2, na.rm = TRUE) +
      labs(x = NULL, y = "mn USD", color = NULL, subtitle = "Quarterly line series") +
      theme_minimal(base_size = 13)

    ggplotly(p, tooltip = "text")
  })

  output$external_balance_plot <- renderPlotly({
    df <- filtered_div(); req(df)
    ca_col <- pick_first_existing(df, c("current_account_balance_mn_usd"))
    tb_col <- pick_first_existing(df, c("trade_balance_mn_usd", "goods_trade_balance_mn_usd"))
    validate(need(!is.null(ca_col) || !is.null(tb_col), "Balance columns not found."))

    cols <- c("period_date", "period_type", ca_col, tb_col)
    cols <- cols[!duplicated(cols) & !is.na(cols)]

    plot_df <- df %>%
      filter(period_type == "quarterly") %>%
      select(all_of(cols)) %>%
      pivot_longer(cols = -c(period_date, period_type), names_to = "metric", values_to = "value") %>%
      mutate(value = suppressWarnings(as.numeric(value))) %>%
      filter(!is.na(value)) %>%
      arrange(metric, period_date) %>%
      mutate(
        metric_label = recode(metric,
          current_account_balance_mn_usd = "Current account balance",
          trade_balance_mn_usd = "Trade balance",
          goods_trade_balance_mn_usd = "Trade balance"
        ),
        hover_text = paste0(
          "Quarter: ", format(period_date, "%Y-%m"),
          "<br>Metric: ", metric_label,
          "<br>Value: ", scales::comma(round(value, 1)), " mn USD"
        )
      )

    validate(need(nrow(plot_df) > 0, "No quarterly current account / trade balance data available."))

    p <- ggplot(plot_df, aes(period_date, value, color = metric_label, group = metric_label, text = hover_text)) +
      geom_hline(yintercept = 0, linetype = "dashed") +
      geom_line(linewidth = 1.3, na.rm = TRUE) +
      geom_point(size = 2.2, na.rm = TRUE) +
      labs(x = NULL, y = "mn USD", color = NULL, subtitle = "Quarterly line series") +
      theme_minimal(base_size = 13)

    ggplotly(p, tooltip = "text")
  })

  output$income_plot <- renderPlotly({
    df <- filtered_div(); req(df)

    wage_col <- pick_first_existing(df, c("avg_monthly_wage_growth_pct", "real_wage_growth_pct", "nominal_wage_growth_pct"))
    inc_col <- pick_first_existing(df, c("nominal_income_growth_pct", "real_income_growth_pct", "household_income_growth_pct"))
    inv_col <- pick_first_existing(df, c("capital_investment_growth_pct", "investment_growth_pct"))

    cols <- c("period_date", "period_type", wage_col, inc_col, inv_col)
    cols <- cols[!duplicated(cols) & !is.na(cols)]

    validate(need(length(cols) > 2, "Monthly wage / income / investment columns not found."))

    yoy_index_metrics <- c(
      "avg_monthly_wage_growth_pct",
      "real_wage_growth_pct",
      "nominal_wage_growth_pct",
      "nominal_income_growth_pct",
      "real_income_growth_pct",
      "household_income_growth_pct",
      "capital_investment_growth_pct",
      "investment_growth_pct"
    )

    plot_df <- df %>%
      filter(period_type == "monthly", period_date >= as.Date("2020-01-01")) %>%
      select(all_of(cols)) %>%
      pivot_longer(cols = -c(period_date, period_type), names_to = "metric", values_to = "value") %>%
      mutate(
        value = suppressWarnings(as.numeric(value)),
        value = if_else(metric %in% yoy_index_metrics & !is.na(value), value - 100, value)
      ) %>%
      filter(!is.na(value)) %>%
      arrange(metric, period_date) %>%
      mutate(
        metric_label = recode(
          metric,
          avg_monthly_wage_growth_pct = "Average monthly wage growth (y/y)",
          real_wage_growth_pct = "Real wage growth (y/y)",
          nominal_wage_growth_pct = "Nominal wage growth (y/y)",
          nominal_income_growth_pct = "Nominal income growth (y/y)",
          real_income_growth_pct = "Real income growth (y/y)",
          household_income_growth_pct = "Household income growth (y/y)",
          capital_investment_growth_pct = "Capital investment growth (y/y)",
          investment_growth_pct = "Investment growth (y/y)"
        ),
        hover_text = paste0(
          "Month: ", format(period_date, "%Y-%m"),
          "<br>Metric: ", metric_label,
          "<br>Value: ", scales::number(value, accuracy = 0.1), "%"
        )
      )

    validate(need(nrow(plot_df) > 1, "Monthly investment / wage dynamics do not have enough non-null observations to draw lines."))

    p <- ggplot(plot_df, aes(period_date, value, color = metric_label, group = metric_label, text = hover_text)) +
      geom_hline(yintercept = 0, linetype = "dashed") +
      geom_line(linewidth = 0.9, na.rm = TRUE) +
      geom_point(size = 1.4, na.rm = TRUE) +
      labs(
        x = NULL,
        y = "%",
        color = NULL,
        subtitle = "Monthly y/y series (2020+, previous year = 100 converted to growth)"
      ) +
      theme_minimal(base_size = 13)

    ggplotly(p, tooltip = "text")
  })

  output$div_table <- renderDT({
    df <- filtered_div(); req(df)
    datatable(df %>% arrange(desc(period_date)), extensions = "Buttons",
              options = list(dom = "Bfrtip", buttons = c("copy", "csv", "excel"), pageLength = 12, scrollX = TRUE))
  })

  output$storyline_text <- renderText({
    paste0(
      "<h4>How to use this for a World Bank CPF-style discussion</h4>",
      "<ol>",
      "<li><b>Macro incentives:</b> show whether inflation, lending rates, and NPL dynamics create or weaken incentives for long-term private investment.</li>",
      "<li><b>Digital inclusion:</b> show whether payment rails, POS density, e-commerce, and mobile banking are lowering friction for households and MSMEs.</li>",
      "<li><b>Structural transformation:</b> compare non-oil GDP growth and non-oil export trends with oil-linked external balances.</li>",
      "<li><b>Institutional cross-check:</b> benchmark Azerbaijan against GDP, governance, and financial inclusion indicators where World Bank-managed datasets are available.</li>",
      "</ol>"
    )
  })

  output$benchmark_table <- renderDT({
    bench <- data_bundle()$benchmark; req(bench)
    datatable(bench %>% arrange(desc(gdp_per_capita)), options = list(pageLength = 15, scrollX = TRUE))
  })
}

shinyApp(ui, server)
