## Exercise 1

Create an app called ``payments``

The app has two models,
- transaction
- file

Let's imagine that we have received a file from the bank with list of transactions they have processed for you.

A transaction might consist of

    - amount
    - account number you paid to
    - reference to which file it was included in

A file has

    - a filename
    - a creation date


1.  Create models for the above entities
2.  Start the Python shell with ./manage.py shell and create some sample data to work with.
3.  Try some queries using the ORM

    - All transactions with amount larger than X
    - All transactions before a specific date
