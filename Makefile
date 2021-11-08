
create_db:
	python3 -c "import manage; manage.create_all()"

delete_filter:
	python3 -c "import manage; manage.delete_filter('$(FILTER)')"

delete_color_map:
	python3 -c "import manage; manage.delete_color_map('$(COLOR_MAP)')"

delete_label:
	python3 -c "import manage; manage.delete_label('$(LABEL)')"