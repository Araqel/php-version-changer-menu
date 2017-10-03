#!/bin/sh

VERSION=$1

if [  $# = 0 ]; then
echo 'Please provide version'
exit;
fi
if [ -z `ls /etc/php | grep $VERSION` ]; then
echo "You don't have php$VERSION version!!"
exit
fi

ls /etc/php | xargs -L1 -I V sudo sh -ic "echo Disabling phpV ...;  a2dismod phpV > /dev/null 2>&1"

echo `$DZYADZ | grep $VERSION`
a2enmod php$VERSION> /dev/null 
echo "Enabled php ${VERSION} mode"

sudo update-alternatives --set php /usr/bin/php${VERSION} > /dev/null 
echo "changed php-cli version to ${VERSION}"

echo 'Restarting Apache2 Service...'
service apache2 restart
echo 'Everything works fine!!!'
