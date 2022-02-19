![snapchat-logo](./docs/snapchat-logo.jpeg)

# About
This is a simple tool for visualizing your Snapchat history location.

# Setup

To start, you'll need to download your saved Snapchat data: https://support.snapchat.com/en-US/a/download-my-data

Unzip it, and extract the file called `location_history.json`. Save it at the root of this repository.

Run:

```bash
$ python analyzer.py
```

When it finishes, open `map.html` in a web browser.

You'll see something that looks like this:

![screenshot](./docs/snapchat-map-screenshot.png)

# Features/Roadmap

- [ ] Save location history to GPX file
- [ ] Create animated maps