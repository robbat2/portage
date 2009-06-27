import logging
import os
import textwrap

# for an explanation on this logic, see pym/_emerge/__init__.py
import os
import sys
if os.environ.__contains__("PORTAGE_PYTHONPATH"):
	sys.path.insert(0, os.environ["PORTAGE_PYTHONPATH"])
else:
	sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pym"))
import portage

from portage.util import writemsg_level

def show_invalid_depstring_notice(parent_node, depstring, error_msg):

	msg1 = "\n\n!!! Invalid or corrupt dependency specification: " + \
		"\n\n%s\n\n%s\n\n%s\n\n" % (error_msg, parent_node, depstring)
	p_type, p_root, p_key, p_status = parent_node
	msg = []
	if p_status == "nomerge":
		category, pf = portage.catsplit(p_key)
		pkg_location = os.path.join(p_root, portage.VDB_PATH, category, pf)
		msg.append("Portage is unable to process the dependencies of the ")
		msg.append("'%s' package. " % p_key)
		msg.append("In order to correct this problem, the package ")
		msg.append("should be uninstalled, reinstalled, or upgraded. ")
		msg.append("As a temporary workaround, the --nodeps option can ")
		msg.append("be used to ignore all dependencies.  For reference, ")
		msg.append("the problematic dependencies can be found in the ")
		msg.append("*DEPEND files located in '%s/'." % pkg_location)
	else:
		msg.append("This package can not be installed. ")
		msg.append("Please notify the '%s' package maintainer " % p_key)
		msg.append("about this problem.")

	msg2 = "".join("%s\n" % line for line in textwrap.wrap("".join(msg), 72))
	writemsg_level(msg1 + msg2, level=logging.ERROR, noiselevel=-1)

