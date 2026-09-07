# Telegram Queuing Bot

Telegram Queuing Bot (further, simply Bot) is a telegram bot for autoscheduling queues for university routines related to completion of laboratory and practice works keeping order which students were stay in.

## Content
0. Purpose and idea;
1. Stack and dependencies;
2. Architecture;
3. Concepts: \
   3.1. Queue; \
   3.2. Discipline; \
   3.3. User; \
   3.4. OACJobs;
4. OAC architecture (OAC State Machine);
5. Key functionality: \
5.1. Autoscheduling; \
5.2. Notifications;
6. External resources;
7. Deployment;

## 0. Purpose and idea

Even though each student has its unique number in the group's list, the final order is up to students themselves. To avoid conflicts in opinions between students, the decision to automate the process of queuing has been made.

The purpose of the developing the project was to automate:
1. Opening, activating, closing queues when the time of practice or laboratory lesson came;
2. Scheduling queues;
3. Notifying users when the lesson starts to motivate them to take their places.

The Bot also supports the additional functions like ability to subscribe/unsubscribe the queues if a user wishes.

## 1. Stack and dependencies

All dependencies are specified in $requirements.txt$ file. The key ones are described below:
1. **python-telegram-bot**. Pure-Python asynchronous library that provides a clean and intuitive interface for the Telegram Bot API. Designed around Python's asyncio framework. Allows to build stateful conversational applications.
2. **aiohttp**. Asynchronous HTTP client and server framework built natively on top of Python's asyncio event loop. It is a foundational library for modern async web development in Python, eliminating the need for multi-threading to handle high I/O concurrency.
3. **APScheduler**. Task scheduling library that allows Python applications to execute periodic or time-delayed jobs. It abstracts the complexities of time management, providing a unified interface to run Python functions at specific intervals or pre-defined cron-like times.

## 2. Architecture

## 3. Concepts

### 3.1. Queue

### 3.2. Discipline

### 3.3. User

### 3.4. OACJobs

## 4. OAC Architecture (OAC State Machine)

According to this architecture, each queue acts as a finite state machine which state is changed at the scheduled time.
The following explains the sense of each state.

### 4.1. Open State

### 4.2. Active State

### 4.3. Closed State

## 5. Key functionality

### 5.1. Autoscheduling

### 5.2. Notifications

## 6. External resources

The university's timetable has no public API.

## 7. Deployment
