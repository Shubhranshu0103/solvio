# SRS Document for Solvio

## Introduction
### Product Scope
Solvio is a personalized learning system

### Intended Audience
Middle School Students (class 6-8)

### Intended Use
- Users should be able to login to the platform
- On an initial assessment, users should be shown the modules they can start learning.
- Choosing a module will direct the user to a number of conceptual articles.
- After reading an article user can select his confidence level on the article
- Midway through the module, a quiz can be consisting of no more than 4 questions
- At the end of the module, a test will be taken covering all the concepts in the module
- Finally, a sneak peek will be shown about the next time this module is visited
- If the module was perfectly learned, a completion screen will appear

### Functional Requirements
- System should have a session/login mechanism
- Each module needs to have pre assessment
  - We need to have a static knowledge space graph of all the modules
- per module "progress" should be stored
- in a module, the notion of "progress" should be captured article wise through quizzes


## Prototype
### Scope
- Only One Module - Properties of Integers
- Module is divided into 3 articles
  - Properties under addition and subtraction
  - Properties under multiplication
  - Properties under division
