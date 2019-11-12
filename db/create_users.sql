drop table if exists users;
create table users(id serial primary key, name varchar);

drop function if exists notify_users_insert();

CREATE FUNCTION notify_users_change() RETURNS TRIGGER AS $BODY$
BEGIN
  IF (TG_OP = 'DELETE') THEN
    perform PG_NOTIFY(
      'channel1',
      'delete from users: ' || OLD.id
    );
    RETURN OLD;
  ELSIF (TG_OP = 'UPDATE') THEN
    perform PG_NOTIFY(
      'channel1',
      'update users: ' || NEW.id || ', ' || NEW.name
    );
  ELSIF (TG_OP = 'INSERT') THEN
    perform PG_NOTIFY(
      'channel1',
      'insert into users: ' || NEW.id || ', ' || NEW.name
    );
    RETURN NEW;
  END IF;
  RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notify_users_change
AFTER INSERT OR UPDATE OR DELETE
ON users
FOR EACH ROW
EXECUTE PROCEDURE notify_users_change();
