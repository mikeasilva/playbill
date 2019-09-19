library(DBI)
library(dplyr)
library(RSQLite)
# Connect to the database
conn <- dbConnect(RSQLite::SQLite(), "playbill.sqlite")
# Extract the variables of interest
df <- dbGetQuery(conn, "SELECT show, theatre, gross, week_ending FROM data") %>%
  rename(current_week = gross) %>%
  mutate(week_ending = as.Date(week_ending))
# Add in the gross revenue from the preceeding week and write a CSV file
df %>%
  rename(past_week = current_week) %>%
  mutate(week_ending = week_ending + 7) %>%
  merge(df) %>%
  select(show, theatre, current_week, past_week, week_ending) %>%
  write.csv(., "playbill.csv", row.names = FALSE)
# Disconnect from the database 
dbDisconnect(conn)