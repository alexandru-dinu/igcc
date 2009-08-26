APP_NAME=igcc
VERSION=0.1
TMP_DIR=/tmp/$(APP_NAME)

pkg-src:
	mkdir -p pkg
	rm -f pkg/$(APP_NAME)-*.tar.bz2
	- rm -r $(TMP_DIR)
	mkdir $(TMP_DIR)
	git archive --format=tar --prefix=$(APP_NAME)-$(VERSION)/ master > pkg/$(APP_NAME)-$(VERSION).tar
	bzip2 pkg/$(APP_NAME)-$(VERSION).tar

