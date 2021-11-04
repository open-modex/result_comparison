
create_db:
	python3 -c "import manage; manage.create_all()"

delete_filter:
	python3 -c "import manage; manage.delete_filter('$(FILTER)')"