---
name: r
detect: ["*.R", "*.Rmd", "*.qmd", "DESCRIPTION", ".Rproj", "renv.lock"]
version: "6.2.1"
category: data
tier: 2
---

# R Patterns — DOMYH Awesome Code

> **Version**: R 4.4+ (2025-2026)
> **Ecosystem**: Tidyverse, Shiny, ggplot2
> **Philosophy**: Data analysis first, reproducibility

---

## 🎯 When to Use This Skill

Use for: Statistical analysis, data visualization, ML modeling, Shiny apps.
**NOT for**: Web backends (→ go/python), mobile (→ flutter).

---

## 📦 Recommended Stack (2025-2026)

### Core Tidyverse

| Package     | Use Case             | Install                       |
| ----------- | -------------------- | ----------------------------- |
| **dplyr**   | Data manipulation 🏆 | `install.packages("dplyr")`   |
| **ggplot2** | Visualization 🏆     | `install.packages("ggplot2")` |
| **tidyr**   | Data tidying         | `install.packages("tidyr")`   |
| **purrr**   | Functional prog      | `install.packages("purrr")`   |
| **readr**   | Fast I/O             | `install.packages("readr")`   |

### Specialized

| Package        | Use Case        | Install                          |
| -------------- | --------------- | -------------------------------- |
| **data.table** | Big data 🏆     | `install.packages("data.table")` |
| **Shiny**      | Web apps        | `install.packages("shiny")`      |
| **tidymodels** | ML pipeline     | `install.packages("tidymodels")` |
| **renv**       | Reproducibility | `install.packages("renv")`       |

---

## 🔄 Tidyverse Patterns

### Data Manipulation with dplyr

```r
library(tidyverse)

# ✅ Pipe-based workflow
result <- data |>
  filter(age >= 18, status == "active") |>
  mutate(
    age_group = case_when(
      age < 30 ~ "young",
      age < 50 ~ "middle",
      TRUE ~ "senior"
    ),
    full_name = paste(first_name, last_name)
  ) |>
  group_by(department) |>
  summarise(
    count = n(),
    avg_salary = mean(salary, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(count))
```

### Joining Data

```r
# ✅ Multiple join types
users_with_orders <- users |>
  left_join(orders, by = "user_id") |>
  left_join(products, by = "product_id")

# ✅ Anti-join: users without orders
users_no_orders <- users |>
  anti_join(orders, by = "user_id")

# ✅ Semi-join: users with orders (no duplicates)
users_with_orders_unique <- users |>
  semi_join(orders, by = "user_id")
```

### Window Functions

```r
data |>
  group_by(department) |>
  mutate(
    rank = row_number(desc(salary)),
    pct_rank = percent_rank(salary),
    cumsum_salary = cumsum(salary),
    lag_salary = lag(salary, 1),
    lead_salary = lead(salary, 1)
  ) |>
  filter(rank <= 3)  # Top 3 per department
```

---

## 📊 ggplot2 Visualization

### Complete Theme

```r
library(ggplot2)

theme_domyh <- function() {
  theme_minimal() +
    theme(
      text = element_text(family = "Inter"),
      plot.title = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12, color = "gray50"),
      axis.title = element_text(size = 11),
      legend.position = "bottom",
      panel.grid.minor = element_blank()
    )
}

# Usage
ggplot(data, aes(x = date, y = value, color = category)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_color_viridis_d() +
  labs(
    title = "Sales Trend",
    subtitle = "Monthly revenue by category",
    x = NULL, y = "Revenue ($M)"
  ) +
  theme_domyh()
```

### Faceted Plots

```r
# ✅ Grid of plots
ggplot(data, aes(x = x, y = y)) +
  geom_point(alpha = 0.6) +
  geom_smooth(method = "loess") +
  facet_wrap(~category, scales = "free_y", ncol = 3) +
  theme_domyh()

# ✅ Two-variable facet
ggplot(data, aes(x = x, y = y)) +
  geom_boxplot() +
  facet_grid(rows = vars(year), cols = vars(region))
```

---

## 🌐 Shiny Web Apps

### Modern Shiny Structure

```r
# app.R
library(shiny)
library(bslib)

ui <- page_navbar(
  theme = bs_theme(
    bootswatch = "flatly",
    primary = "#0d6efd"
  ),
  title = "Dashboard",

  nav_panel("Overview",
    layout_sidebar(
      sidebar = sidebar(
        selectInput("department", "Department", choices = NULL),
        dateRangeInput("dates", "Date Range")
      ),
      card(
        card_header("Key Metrics"),
        plotOutput("main_plot")
      )
    )
  ),

  nav_panel("Details",
    DT::dataTableOutput("details_table")
  )
)

server <- function(input, output, session) {
  # Reactive data
  filtered_data <- reactive({
    data |>
      filter(
        department == input$department,
        date >= input$dates[1],
        date <= input$dates[2]
      )
  })

  # Update choices on load
  observe({
    updateSelectInput(session, "department",
                      choices = unique(data$department))
  })

  # Outputs
  output$main_plot <- renderPlot({
    filtered_data() |>
      ggplot(aes(x = date, y = value)) +
      geom_line() +
      theme_domyh()
  })

  output$details_table <- DT::renderDataTable({
    filtered_data()
  })
}

shinyApp(ui, server)
```

---

## 🤖 tidymodels ML Pipeline

```r
library(tidymodels)

# ✅ Complete ML workflow
set.seed(123)

# Split data
splits <- initial_split(data, prop = 0.8, strata = outcome)
train_data <- training(splits)
test_data <- testing(splits)

# Recipe (preprocessing)
recipe <- recipe(outcome ~ ., data = train_data) |>
  step_normalize(all_numeric_predictors()) |>
  step_dummy(all_nominal_predictors()) |>
  step_zv(all_predictors())

# Model specification
rf_spec <- rand_forest(
  mtry = tune(),
  trees = 500,
  min_n = tune()
) |>
  set_engine("ranger") |>
  set_mode("classification")

# Workflow
rf_workflow <- workflow() |>
  add_recipe(recipe) |>
  add_model(rf_spec)

# Cross-validation
cv_folds <- vfold_cv(train_data, v = 5, strata = outcome)

# Tune hyperparameters
rf_tune <- rf_workflow |>
  tune_grid(
    resamples = cv_folds,
    grid = 20,
    metrics = metric_set(roc_auc, accuracy)
  )

# Best model
best_params <- select_best(rf_tune, metric = "roc_auc")
final_workflow <- finalize_workflow(rf_workflow, best_params)

# Fit final model
final_fit <- fit(final_workflow, train_data)

# Evaluate on test
predictions <- predict(final_fit, test_data, type = "prob") |>
  bind_cols(test_data)

roc_auc(predictions, truth = outcome, .pred_class_1)
```

---

## 📦 Package Development

```r
# Create package structure
usethis::create_package("mypackage")
usethis::use_mit_license()
usethis::use_testthat()
usethis::use_pipe()

# Add dependencies
usethis::use_package("dplyr")
usethis::use_package("ggplot2", type = "Suggests")

# Document with roxygen2
#' Calculate summary statistics
#'
#' @param data A data frame
#' @param group_var Grouping variable (unquoted)
#' @param value_var Value variable (unquoted)
#' @return A tibble with summary statistics
#' @export
#' @examples
#' summarize_data(mtcars, cyl, mpg)
summarize_data <- function(data, group_var, value_var) {
  data |>
    dplyr::group_by({{ group_var }}) |>
    dplyr::summarise(
      mean = mean({{ value_var }}, na.rm = TRUE),
      sd = sd({{ value_var }}, na.rm = TRUE),
      n = dplyr::n(),
      .groups = "drop"
    )
}
```

---

## ✅ Production Checklist

### Code Quality

- [ ] `lintr::lint_package()` passing
- [ ] `R CMD check` with no errors
- [ ] roxygen2 documentation complete
- [ ] Style follows tidyverse style guide

### Reproducibility

- [ ] renv.lock committed
- [ ] Seeds set for random operations
- [ ] Quarto/RMarkdown for reports
- [ ] Docker for deployment

### Testing

- [ ] testthat tests written
- [ ] Coverage > 70%
- [ ] Integration tests for Shiny

---

_DOMYH Awesome Code • R 4.4+ Tidyverse_
