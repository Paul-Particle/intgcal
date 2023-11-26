# intgcal

## Project Description

Schedule Intend.do lists on Google Calendar.  

This command line tool turns properly formatted task lists into `.ics` files
with events representing those tasks. The task lists are 'intention' lists, as
the [intend.do](https://intend.do/) tool uses the term. The `.ics` files can
then be imported into Google Calendar with another tool, `gcalcli`, which needs
to be [installed](https://github.com/insanum/gcalcli) separately.

The main use of this tool is to visualize the amount of planned work to notice
when you plan too much for one day. Warnings will be issued if the workload
seems too high. 

I suggest constantly adjusting events while working. This way they reflect when
you really started and how long things really took. At the end of the day, this
enables you to compare the planned durations to the actual ones, when reviewing
outcomes in Intend, where the original estimate appears in the intentions of
the day.

## Usage

`intgcal path/to/task_list`

In `task_list.txt`, list intentions for the day, one per line. Add the
estimated duration of the intention in minutes enclosed in brackets after the
description. 

Example: `1) Work on report [120]` would generate 120 minute event at the next
full quarter hour in the calendar `1) Work` as per the default `config.json`.

Options:

- `--import-gcalcli`: Actually to the import, by default only `.ics` files are
  generated.
- `--end-time`: Set the time after which no task is to be scheduled (format
  HH:MM). Default is set in `config.json`.
- `--start-time`: Specify a start time. (format HH:MM) Default is next full
  quarter hour.

Use `config.json` to set up the mapping between goals and calendars. For each
goal prefix one `.ics` file is created. Automatic import of `.ics` files is done
with `gcalcli` (install separately, including vobject required for the import
functionality). 

## Installation

Note: These instructions are specific to MacOS and potentially idiosyncratic.

1. Clone or download the project directory.
2. Create a Python virtual environment: `conda create intgcal_venv` and
   activate it by running `conda activate intgcal_env`.
3. Configure `config.json` with your calendar names and task list prefixes.
4. Install `intgcal`: Navigate to the project root and run `pip install .`
5. Install `gcalcli`: `brew install gcalcli`
6. Install `vobject` for gcalcli: `pip install vobject`
   - Note: You might need to add `--break-system-packages` due to Homebrew's Python management.
7. Set up `gcalcli` following the instructions in its repository.

