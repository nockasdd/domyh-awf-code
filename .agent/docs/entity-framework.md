---
library: entity-framework
version: 9.x
latest: true
category: database
official_docs: https://learn.microsoft.com/en-us/ef/core/
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/dotnet/EntityFramework.Docs/contents/entity-framework/core/get-started
---

# Getting Started with Windows Forms

This step-by-step walkthrough shows how to build a simple Windows Forms (WinForms) application backed by a SQLite database. The application uses Entity Framework Core (EF Core) to load data from the database, track changes made to that data, and persist those changes back to the database.

The screen shots and code listings in this walkthrough are taken from Visual Studio 2022 17.3.0.

> [!TIP]
> You can view this article's [sample on GitHub](https://github.com/dotnet/EntityFramework.Docs/tree/main/samples/core/WinForms).


## Prerequisites

You need to have Visual Studio 2022 17.3 or later installed with the **.NET desktop workload** selected to complete this walkthrough. For more information about installing the latest version of Visual Studio, see [Install Visual Studio](/visualstudio/install/install-visual-studio).


## Install the EF Core NuGet packages

1. Right-click on the solution and choose **Manage NuGet Packages for Solution...**

   ![Manage NuGet Packages for Solution](_static/winforms-manage-nuget.png)

2. Choose the **Browse** tab and search for "Microsoft.EntityFrameworkCore.Sqlite".
3. Select the **Microsoft.EntityFrameworkCore.Sqlite** package.
4. Check the project **GetStartedWinForms** in the right pane.
5. Choose the latest version. To use a pre-release version, make sure that the **Include prerelease** box is checked.
6. Click **Install**

   ![Install the Microsoft.EntityFrameworkCore.Sqlite package](_static/winforms-install-package.png)

> [!NOTE]
> The **Microsoft.EntityFrameworkCore.Sqlite** is the "database provider" package for using EF Core with a SQLite database. Similar packages are available for other database systems. Installing a database provider package automatically brings in all the dependencies needed to use EF Core with that database system. This includes the **Microsoft.EntityFrameworkCore** base package.


## Configuring what is displayed

By default, a column is created in the `DataGridView` for every property of the bound types. Also, the values for each of these properties can be edited by the user. However, some values, such as the primary key values, are conceptually read-only, and so should not be edited. Also, some properties, such as the `CategoryId` foreign key property and the `Category` navigation are not useful to the user, and so should be hidden.

> [!TIP]
> It is common to hide primary key properties in a real application. They are left visible here to make it easy to see what EF Core is doing behind the scenes.

1. Right-click on the first `DataGridView` and choose **Edit Columns...**.

   ![Edit DataGridView columns](_static/winforms-edit-columns.png)

2. Make the `CategoryId` column, which represents the primary key, read-only, and click **OK**.

   ![Make CategoryId column read-only](_static/winforms-categoryid-read-only.png)

3. Right-click on the second `DataGridView` and choose **Edit Columns...**. Make the `ProductId` column read-only, and remove the `CategoryId` and `Category` columns, then click **OK**.

   ![Make ProductId column read-only and remove CategoryId and Category columns](_static/winforms-product-columns.png)


# Getting Started with WPF

This step-by-step walkthrough shows how to bind POCO types to WPF controls in a "main-detail" form. The application uses the Entity Framework APIs to populate objects with data from the database, track changes, and persist data to the database.

The model defines two types that participate in one-to-many relationship: **Category** (principal\\main) and **Product** (dependent\\detail). The WPF data-binding framework enables navigation between related objects: selecting rows in the master view causes the detail view to update with the corresponding child data.

The screen shots and code listings in this walkthrough are taken from Visual Studio 2019 16.6.5.

> [!TIP]
> You can view this article's [sample on GitHub](https://github.com/dotnet/EntityFramework.Docs/tree/main/samples/core/WPF).


## Install the Entity Framework NuGet packages

1. Right-click on the solution and choose **Manage NuGet Packages for Solution...**

    ![Manage NuGet Packages](_static/wpf-tutorial-nuget.jpg)

1. Type `entityframeworkcore.sqlite` in the search box.
1. Select the **Microsoft.EntityFrameworkCore.Sqlite** package.
1. Check the project in the right pane and click **Install**

    ![Sqlite Package](_static/wpf-tutorial-sqlite.jpg)

1. Repeat the steps to search for `entityframeworkcore.proxies` and install **Microsoft.EntityFrameworkCore.Proxies**.

> [!NOTE]
> When you installed the Sqlite package, it automatically pulled down the related **Microsoft.EntityFrameworkCore** base package. The **Microsoft.EntityFrameworkCore.Proxies** package provides support for "lazy-loading" data. This means when you have entities with child entities, only the parents are fetched on the initial load. The proxies detect when an attempt to access the child entities is made and automatically loads them on demand.
