import logging
from django.db import models
from django.db import connection
import os
from django.conf import settings

logger = logging.getLogger(__name__)


class QuerySetManager(models.Manager):
    """
    @see http://djangosnippets.org/snippets/734/
    @see http://hunterford.me/django-custom-model-manager-chaining/
    """
    def get_queryset(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, name, *args):
        if name.startswith('_'):
            raise AttributeError
        return getattr(self.get_queryset(), name, *args)


class LockingManager(models.Manager):
    """
    Add lock/unlock functionality to manager.

    Example::

        class Job(models.Model):

            manager = LockingManager()

            counter = models.IntegerField(null=True, default=0)

            @staticmethod
            def do_atomic_update(job_id)
                ''' Updates job integer, keeping it below 5 '''
                try:
                    # Ensure only one HTTP request can do this update at once.
                    Job.objects.lock()

                    job = Job.object.get(id=job_id)
                    # If we don't lock the tables two simultanous
                    # requests might both increase the counter
                    # going over 5
                    if job.counter < 5:
                        job.counter += 1
                        job.save()

                finally:
                    Job.objects.unlock()

    @see http://djangosnippets.org/snippets/833/
    """

    def lock(self, *args):
        """
        Lock table(s).

        Locks the object model table so that atomic update is possible.
        Simulatenous database access request pend until the lock is unlock()'ed.

        See http://dev.mysql.com/doc/refman/5.0/en/lock-tables.html

        @param *args: Models to be locked - if None then self.model is used.
        """
        if not args:
            args = [self.model]
        cursor = connection.cursor()
        tables = ", ".join(['%s WRITE' % connection.ops.quote_name(model._meta.db_table) for model in args])
        logger.debug('LOCK TABLES %s' % tables)
        cursor.execute("LOCK TABLES %s" % tables)
        row = cursor.fetchone()
        return row

    def unlock(self):
        """
        Unlock the table(s)
        """
        cursor = connection.cursor()
        cursor.execute("UNLOCK TABLES")
        logger.debug('Unlocked tables')
        row = cursor.fetchone()
        return row


class LockingQuerySetManager(QuerySetManager, LockingManager):
    pass


def upload_to(path, filename):
    try:
        _dir = os.path.join(settings.MEDIA_ROOT, path)
        os.makedirs(dir, settings.FILE_UPLOAD_PERMISSIONS)
    except OSError:
        # Someone beat us to the punch
        if not os.path.isdir(_dir):
            # Nope, must be something else...
            raise
    return os.path.join(path, filename)
