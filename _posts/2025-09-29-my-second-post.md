---
layout: post
title: My Second Post
date: '2025-09-29 01:22:01 +0530'
categories: [TOP_CATEGORY, SUB_CATEGORY]
tags: [linux]
image: 
    path: https://avatars.githubusercontent.com/u/90672297?s=400&u=5d7ba147c3d2ced7fb5ddc41afd1b24a173ae58d&v=4
    alt: avatar
description: "This is a custom description that will appear on the home page card and in search results."  
author: sanjay0302
toc: true
comments: true
# media_subpath: /path/to/media/
# To specify the resource path prefix for the current post/page range, set media_subpath in the front matter of the post:
---

# YouTube Embed Test Cases

Complete test suite for the YouTube embed include file with all parameter combinations.

---

## Test Case 1: Basic Embed (Default Settings)


{% include embed/youtube.html id='LJBQ29h7rMM' %}


**Expected Behavior:**
- All default parameters applied
- No autoplay, no loop, controls visible
- Red progress bar, fullscreen enabled

---

## Test Case 2: Loop Single Video


{% include embed/youtube.html id='LJBQ29h7rMM' loop=1 %}


**Expected Behavior:**
- Video loops continuously
- Playlist parameter automatically set to video ID
- URL contains: `loop=1&playlist=LJBQ29h7rMM`

---

## Test Case 3: Playlist with Next Videos (No Loop)


{% include embed/youtube.html id='LJBQ29h7rMM' next_id='qhs-xppFRgE,abc123' %}


**Expected Behavior:**
- Plays main video first, then next videos in sequence
- Main video ID prepended to playlist automatically
- URL contains: `playlist=LJBQ29h7rMM,qhs-xppFRgE,abc123`

---

## Test Case 4: Loop with Playlist


{% include embed/youtube.html id='LJBQ29h7rMM' loop=1 next_id='qhs-xppFRgE,abc123' %}


**Expected Behavior:**
- Entire playlist loops continuously
- All videos play in sequence, then repeat
- URL contains: `loop=1&playlist=LJBQ29h7rMM,qhs-xppFRgE,abc123`

---

## Test Case 5: Autoplay with Mute


{% include embed/youtube.html id='LJBQ29h7rMM' autoplay=1 mute=1 %}


**Expected Behavior:**
- Video starts playing automatically on page load
- Audio is muted (required for autoplay in most browsers)
- URL contains: `autoplay=1&mute=1`

---

## Test Case 6: Custom Color (White Progress Bar)


{% include embed/youtube.html id='LJBQ29h7rMM' color='white' %}


**Expected Behavior:**
- Progress bar and controls use white color scheme
- Valid values: 'red' or 'white'
- URL contains: `color=white`

---

## Test Case 7: Hide Controls


{% include embed/youtube.html id='LJBQ29h7rMM' controls=0 %}


**Expected Behavior:**
- Player controls are hidden
- Video can still be controlled via API or keyboard
- URL contains: `controls=0`

---

## Test Case 8: Start at Specific Time


{% include embed/youtube.html id='LJBQ29h7rMM' start=30 %}


**Expected Behavior:**
- Video begins playing at 30 seconds
- Value in seconds (positive integer)
- URL contains: `start=30`

---

## Test Case 9: End at Specific Time


{% include embed/youtube.html id='LJBQ29h7rMM' end=60 %}


**Expected Behavior:**
- Video stops playing at 60 seconds
- Value in seconds (positive integer)
- URL contains: `end=60`

---

## Test Case 10: Time Range (Start + End)


{% include embed/youtube.html id='LJBQ29h7rMM' start=10 end=50 %}


**Expected Behavior:**
- Video plays from 10 seconds to 50 seconds
- Creates a 40-second clip
- URL contains: `start=10&end=50`

---

## Test Case 11: Closed Captions Enabled


{% include embed/youtube.html id='LJBQ29h7rMM' cc_load_policy=1 %}


**Expected Behavior:**
- Closed captions displayed by default (if available)
- User can still toggle captions off
- URL contains: `cc_load_policy=1`

---

## Test Case 12: Disable Keyboard Controls


{% include embed/youtube.html id='LJBQ29h7rMM' disablekb=1 %}


**Expected Behavior:**
- Keyboard shortcuts disabled (space, arrows, etc.)
- Mouse controls still work
- URL contains: `disablekb=1`

---

## Test Case 13: Disable Fullscreen Button


{% include embed/youtube.html id='LJBQ29h7rMM' fs=0 %}


**Expected Behavior:**
- Fullscreen button hidden from controls
- Video remains in embedded size
- URL contains: `fs=0`

---

## Test Case 14: Show Related Videos from Any Channel


{% include embed/youtube.html id='LJBQ29h7rMM' rel=1 %}


**Expected Behavior:**
- After video ends, shows related videos from all channels
- Default (rel=0) only shows videos from same channel
- URL contains: `rel=1`

---

## Test Case 15: iOS Inline Playback


{% include embed/youtube.html id='LJBQ29h7rMM' playsinline=1 %}


**Expected Behavior:**
- Video plays inline on iOS devices instead of fullscreen
- Only affects iOS Safari
- URL contains: `playsinline=1`

---

## Test Case 16: Complex Combination - Auto-looping Clip


{% include embed/youtube.html id='LJBQ29h7rMM' mute=1 fs=0 autoplay=1 loop=1 start=30 end=35 %}


**Expected Behavior:**
- Autoplays muted from 30s to 35s
- Loops the 5-second clip continuously
- No fullscreen button
- Perfect for background video clips

---

## Test Case 17: Multi-video Playlist


{% include embed/youtube.html id="LJBQ29h7rMM" fs=0 next_id="qhs-xppFRgE,gKWjGVWGCgo,hmUyEDG7Jy0" %}


**Expected Behavior:**
- Plays 4 videos in sequence
- No fullscreen button
- Stops after last video (no loop)
- URL contains: `playlist=LJBQ29h7rMM,qhs-xppFRgE,gKWjGVWGCgo,hmUyEDG7Jy0`

---

## Test Case 18: Looping Playlist


{% include embed/youtube.html id="LJBQ29h7rMM" fs=0 next_id="qhs-xppFRgE,gKWjGVWGCgo" loop=1 %}


**Expected Behavior:**
- Plays 3 videos in sequence
- After last video, returns to first and repeats
- No fullscreen button
- URL contains: `loop=1&playlist=LJBQ29h7rMM,qhs-xppFRgE,gKWjGVWGCgo`

---

## Test Case 19: Multiple Embeds on Same Page

```liquid
{% raw %}
{% include embed/youtube.html id='LJBQ29h7rMM' %}
{% endraw %}
```

```liquid
{% include embed/youtube.html id='LJBQ29h7rMM' %}
```

{% include embed/youtube.html id='LJBQ29h7rMM' loop=1 %}

{% include embed/youtube.html id='qhs-xppFRgE' next_id='video4,video5' %}


**Expected Behavior:**
- All three embeds work independently
- Each has its own configuration
- No conflicts or interference between embeds

---

## Test Case 20: Minimal Embed (Clean Player)


{% include embed/youtube.html id='LJBQ29h7rMM' controls=0 rel=0 disablekb=1 %}


**Expected Behavior:**
- Minimal interface with no controls
- No related videos shown
- No keyboard interaction
- Clean, distraction-free viewing

---

## Test Case 21: Presentation Mode


{% include embed/youtube.html id='LJBQ29h7rMM' autoplay=1 mute=1 controls=0 loop=1 %}


**Expected Behavior:**
- Auto-plays muted in a loop
- No visible controls
- Perfect for background/ambient video in presentations

---

## Test Case 22: Accessible Video


{% include embed/youtube.html id='LJBQ29h7rMM' cc_load_policy=1 controls=1 %}


**Expected Behavior:**
- Captions enabled by default
- Full controls available
- Keyboard navigation enabled (default)
- Optimized for accessibility

---

## Notes

- **Autoplay Limitation**: `autoplay=1` only works reliably when `mute=1` is also set (browser policy)
- **Loop Requirement**: `loop=1` requires a `playlist` parameter, which is automatically added by the code
- **Color Options**: Only 'red' (default) and 'white' are valid values
- **Time Values**: `start` and `end` accept positive integers (seconds)
- **Playlist Order**: Main video ID is always prepended automatically to `next_id`

---

## Quick Reference

| Parameter        | Type             | Default      | Description                               |
| ---------------- | ---------------- | ------------ | ----------------------------------------- |
| `id`             | string           | **required** | YouTube video ID                          |
| `autoplay`       | 0 or 1           | 0            | Auto-play on load (needs mute=1)          |
| `cc_load_policy` | 0 or 1           | 0            | Show captions by default                  |
| `color`          | 'red' or 'white' | 'red'        | Progress bar color                        |
| `controls`       | 0 or 1           | 1            | Show player controls                      |
| `disablekb`      | 0 or 1           | 0            | Disable keyboard controls                 |
| `end`            | integer          | 0            | End time in seconds                       |
| `fs`             | 0 or 1           | 1            | Show fullscreen button                    |
| `loop`           | 0 or 1           | 0            | Loop video/playlist                       |
| `mute`           | 0 or 1           | 0            | Start muted                               |
| `playsinline`    | 0 or 1           | 0            | iOS inline playback                       |
| `rel`            | 0 or 1           | 0            | Show related videos (0=same channel only) |
| `start`          | integer          | 0            | Start time in seconds                     |
| `next_id`        | string           | empty        | Comma-separated video IDs for playlist    |
