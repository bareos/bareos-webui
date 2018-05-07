This repository has been merged into https://github.com/bareos/bareos

The Bareos project consists of several sub projects. While these subprojects
have been kept in different git repositories until bareos <= 17.2, we decided
to merge them all into https://github.com/bareos/bareos

Subprojects:
  * https://github.com/bareos/bareos (core, daemons) repository hasn't changed,
    but its content has been moved to the core subdirectory
    https://github.com/bareos/bareos/tree/master/core/
  * https://github.com/bareos/bareos-docs (master) =>
    https://github.com/bareos/bareos/tree/master/docs/
  * https://github.com/bareos/bareos-regress (master) => https://github.com/bareos/bareos/tree/master/regress/
  * https://github.com/bareos/bareos-vmware (master) => https://github.com/bareos/bareos/tree/master/vmware/
  * https://github.com/bareos/bareos-webui (master) => https://github.com/bareos/bareos/tree/master/webui/
  * https://github.com/bareos/python-bareos (master) => https://github.com/bareos/bareos/tree/master/python-bareos/

We only merged the master branches, so all those plus all future branches from
bareos-18.2 onwards can be found there. The old branches (bareos <= 17.2) will
be kept and maintained in the old repositories.



