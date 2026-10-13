
from datetime import datetime, timedelta


class Task:
    def __init__(
        self,
        task_id,
        title,
        description,
        due_datetime,
        delete_datetime=None,
        completed=False,
        notified=False,
        recurring=False,
    ):
        self._id=task_id
        self.title=title
        self.description=description
        self.due_datetime=due_datetime
        self.delete_datetime=delete_datetime
        self._completed=completed
        self._notified=notified
        self._recurring=recurring
        self._validate()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def completed(self):
        return self._completed

    @property
    def notified(self):
        return self._notified

    @property
    def recurring(self):
        return self._recurring

    def _validate(self):
        if not isinstance(self.due_datetime, datetime):
            raise ValueError("A valid due datetime is required.")

        if self.delete_datetime is not None:
            if not isinstance(self.delete_datetime, datetime):
                raise ValueError("Invalid delete datetime.")

            if self.delete_datetime<=self.due_datetime:
                raise ValueError("Delete time must be after the due time.")

    @staticmethod
    def validate_duration(duration):
        if not isinstance(duration, timedelta):
            raise ValueError("Duration must be a timedelta.")

        if duration.total_seconds() <= 0:
            raise ValueError("Duration must be greater than zero.")

    def complete(self):
        self._completed = True

    def mark_notified(self):
        self._notified = True

    def reschedule(self,next_due_datetime=None):
        if not self._recurring:
            raise ValueError("This task does not repeat.")

        if next_due_datetime is None:
            next_due_datetime = (self.due_datetime+timedelta(days=1))

        if not isinstance(next_due_datetime,datetime):
            raise ValueError("Invalid next due datetime.")

        if next_due_datetime <= self.due_datetime:
            raise ValueError("Next due time must be later than the current due time.")

        if (self.delete_datetime is not None and next_due_datetime >= self.delete_datetime
        ):
            raise ValueError("The task has reached its delete time.")

        self.due_datetime = next_due_datetime
        self._notified = False

    def is_expired(self,current_time):
        return (self.delete_datetime is not None and current_time >= self.delete_datetime
        )
