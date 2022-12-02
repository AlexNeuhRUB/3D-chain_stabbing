library("rjson")
library("ggpubr")
library("tidyverse")

frame <- data.frame(method=c(), track=c(), epsilon=c(), radius=c(), time=c(), input_len=c(), output_len=c())

files <- list.files("./fred")
for (file in files) {
  file <- paste(getwd(), "/fred/" , file, "/results.json", sep="")
  print(file)
  method <- "fred"
  json_data <- fromJSON(file=file)
  epsilon <- json_data$epsilon
  track <- json_data$`Track ID`
  radius <- json_data$radius
  time <- json_data$`running time (secs)`
  input_len <- json_data$`Input size`
  output_len <- json_data$`Output size`
  for (i in 1:length(epsilon)) {
    df <- data.frame(method=method, track=track[[i]], epsilon=epsilon[[i]], radius=radius[[i]], time=time[[i]]/60, input_len=input_len[[i]], output_len=output_len[[i]])
    frame <- rbind(frame, df)
  }
}

files <- list.files("./stabbing")
for (file in files) {
  file <- paste(getwd(), "/stabbing/" , file, "/results.json", sep="")
  print(file)
  method <- "stabbing"
  json_data <- fromJSON(file=file)
  epsilon <- json_data$epsilon
  track <- json_data$`Track ID`
  radius <- json_data$radius
  time <- json_data$`running time (secs)`
  input_len <- json_data$`Input size`
  output_len <- json_data$`Output size`
  for (i in 1:length(epsilon)) {
    df <- data.frame(method=method, track=track[[i]], epsilon=epsilon[[i]], radius=radius[[i]], time=time[[i]]/60, input_len=input_len[[i]], output_len=output_len[[i]])
    frame <- rbind(frame, df)
  }
}

gdata <- frame %>%
  group_by_at(vars(track, epsilon)) %>%
  mutate(Data = paste("Track", track, sep=" ")) %>%
  filter(method == "stabbing")

fdata <- frame %>%
  group_by_at(vars(track, epsilon)) %>%
  mutate(Data = paste("Track", track, sep=" ")) %>%
  filter(method == "fred") %>%
  summarise(mtime = mean(time), sdtime = sd(time))

ggplot(gdata, aes(factor(epsilon), time)) + 
  geom_boxplot(aes(color = Data), outlier.alpha=0.5) +
  scale_y_continuous(trans='log10', name = "time [min]") +
  scale_x_discrete(name = "epsilon")

