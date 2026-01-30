## 1. Core Concept: Group

In this project, the **Group** is the core data organization concept.

The data model is organized into three levels:

- Group
- Unit
- Unit data

The smallest meaningful group (i.e. a single unit) is a collection of financial income and expense records, which is equivalent to a table.  
A Group represents the aggregation of all its units.

---

## 2. The Smallest Structure of a Group: Unit

Each unit can be considered an independent table.  
The structure of a unit (expense unit) and example data are shown below:

|id|category|subcategory|item|io|amount|
|---|---|---|---|---|---|
|1|Food|Main meals|Tomato beef pasta|O|19.00|
|2|Daily|Services|Mobile recharge|O|98.00|
|3|Special|Clothing|Linen shirt|O|168.00|

- `IO` indicates income or expense:
    - `I` = Income
    - `O` = Outcome (Expense)

---

## 3. Project Directory

A project directory is a folder stored under the `data` directory.  
It contains all the basic data of a project. Each time the program starts, a project directory must be selected before any operation can be performed.

### 3.1 Project Directory Structure

Each project directory contains only one type of file:

- `[No]_[unit name].csv`: source data of a unit

Notes:

- The CSV filename **must start with a numeric index followed by an underscore**
- The numeric indices must form a **continuous, increasing sequence starting from 1**
- This sequence represents the logical order of units

### 3.2 Loading a Project

When a project directory is selected and loaded, the program reads each CSV file, converts every unit into a DataFrame, and then merges all unit DataFrames into a single Group DataFrame.

CSV is used as the storage format primarily for compatibility reasons.

You can inspect the implementation details in the `load_project_by_id()` function located in  
`src/core/project_manager.py`.

---

## 4. Analysis Modes

All units within a project are combined into a Group, which is the largest data structure in the program.

The program supports four analysis modes:

1. **Unit analysis**  
    Perform calculations and analysis on a specific unit only.
    
2. **Unit point-to-point horizontal analysis**  
    Compare and analyze two units.
    
3. **Group horizontal analysis**  
    Compare and analyze all units within a group.
    
4. **Vertical merged analysis**  
    Merge all units into a single dataset and perform calculations and analysis on the entire group.

---

## 5. Analysis Plugins

The main program is only responsible for menu interaction, basic configuration, and providing DataFrame data.  
All actual analysis logic is fully delegated to plugins.

### 5.1 What Is an Analysis Plugin

As described above, analysis strategies and execution logic are determined by analysis plugins.  
Plugins are Python (`.py`) files located in the `src/plugins` directory.

### 5.2 Plugin File Naming

In the plugins directory, you may see filenames such as:

```
[Default] Basic.py
```

- The name inside the square brackets represents the plugin category
- `Basic` is the plugin name

This naming convention is **recommended but not mandatory**.

---

## 6. Built-in Plugin

For various reasons, only one built-in plugin was implemented, and it was not fully completed.  
Originally, at least two or more plugins were planned.

The good news is that this plugin already provides a complete framework.  
If you want to improve it or create new plugins, you can simply modify or extend this plugin as a base.

The plugin is named `[Default] Basic.py` and is the only `.py` file in the plugins directory.

In this plugin:

- Each unit represents all financial records for a single month
- A group represents all financial records for an entire year

Another planned plugin would have treated each unit as a major category  
(e.g. daily expenses, installment payments, investment income/expenses),  
with a group representing a month or a year.

Unfortunately, this plugin was not completed.

---

## 7. Conclusion

The goal of this project is not to build a fully featured financial system, but to explore a **scalable and replaceable analysis architecture** through clear data layering (Group / Unit) and a plugin-based analysis mechanism.

Although the project remains relatively immature in terms of engineering completeness, it has successfully fulfilled its role as an exploratory experimental project for an amateur Python developer.

The current implementation covers only the most basic use cases, but the core design is complete:  
the data structure is stable, analysis logic is decoupled, and plugins are freely extensible.  
Future improvements—whether enhancing existing plugins or introducing new analysis paradigms—can be achieved without modifying the main program.
