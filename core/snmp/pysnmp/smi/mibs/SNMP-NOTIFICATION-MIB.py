# PySNMP SMI module. Autogenerated from smidump -f python SNMP-NOTIFICATION-MIB
# by libsmi2pysnmp-0.0.9-alpha at Thu Mar 26 20:58:12 2009,
# Python version (2, 4, 4, 'final', 0)

# Imported just in case new ASN.1 types would be created
from pyasn1.type import constraint, namedval

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( SnmpTagValue, snmpTargetBasicGroup, snmpTargetBasicGroup, snmpTargetBasicGroup, snmpTargetParamsMPModel, snmpTargetParamsName, snmpTargetParamsRowStatus, snmpTargetParamsSecurityLevel, snmpTargetParamsSecurityModel, snmpTargetParamsSecurityName, snmpTargetParamsStorageType, snmpTargetResponseGroup, ) = mibBuilder.importSymbols("SNMP-TARGET-MIB", "SnmpTagValue", "snmpTargetBasicGroup", "snmpTargetBasicGroup", "snmpTargetBasicGroup", "snmpTargetParamsMPModel", "snmpTargetParamsName", "snmpTargetParamsRowStatus", "snmpTargetParamsSecurityLevel", "snmpTargetParamsSecurityModel", "snmpTargetParamsSecurityName", "snmpTargetParamsStorageType", "snmpTargetResponseGroup")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Integer32, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, snmpModules, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "snmpModules")
( RowStatus, StorageType, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "StorageType")

# Objects

snmpNotificationMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 13)).setRevisions(("2002-10-14 00:00","1998-08-04 00:00","1997-07-14 00:00",))
if mibBuilder.loadTexts: snmpNotificationMIB.setOrganization("IETF SNMPv3 Working Group")
if mibBuilder.loadTexts: snmpNotificationMIB.setContactInfo("WG-email:   snmpv3@lists.tislabs.com\nSubscribe:  majordomo@lists.tislabs.com\n            In message body:  subscribe snmpv3\n\nCo-Chair:   Russ Mundy\n            Network Associates Laboratories\nPostal:     15204 Omega Drive, Suite 300\n            Rockville, MD 20850-4601\n            USA\nEMail:      mundy@tislabs.com\nPhone:      +1 301-947-7107\n\nCo-Chair:   David Harrington\n            Enterasys Networks\nPostal:     35 Industrial Way\n            P. O. Box 5004\n            Rochester, New Hampshire 03866-5005\n            USA\nEMail:      dbh@enterasys.com\nPhone:      +1 603-337-2614\n\nCo-editor:  David B. Levi\n            Nortel Networks\nPostal:     3505 Kesterwood Drive\n            Knoxville, Tennessee 37918\nEMail:      dlevi@nortelnetworks.com\nPhone:      +1 865 686 0432\n\nCo-editor:  Paul Meyer\n            Secure Computing Corporation\nPostal:     2675 Long Lake Road\n            Roseville, Minnesota 55113\nEMail:      paul_meyer@securecomputing.com\nPhone:      +1 651 628 1592\n\nCo-editor:  Bob Stewart\n            Retired")
if mibBuilder.loadTexts: snmpNotificationMIB.setDescription("This MIB module defines MIB objects which provide\nmechanisms to remotely configure the parameters\nused by an SNMP entity for the generation of\nnotifications.\n\nCopyright (C) The Internet Society (2002). This\nversion of this MIB module is part of RFC 3413;\nsee the RFC itself for full legal notices.")
snmpNotifyObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 1))
snmpNotifyTable = MibTable((1, 3, 6, 1, 6, 3, 13, 1, 1))
if mibBuilder.loadTexts: snmpNotifyTable.setDescription("This table is used to select management targets which should\nreceive notifications, as well as the type of notification\nwhich should be sent to each selected management target.")
snmpNotifyEntry = MibTableRow((1, 3, 6, 1, 6, 3, 13, 1, 1, 1)).setIndexNames((1, "SNMP-NOTIFICATION-MIB", "snmpNotifyName"))
if mibBuilder.loadTexts: snmpNotifyEntry.setDescription("An entry in this table selects a set of management targets\nwhich should receive notifications, as well as the type of\n\n\n\nnotification which should be sent to each selected\nmanagement target.\n\nEntries in the snmpNotifyTable are created and\ndeleted using the snmpNotifyRowStatus object.")
snmpNotifyName = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 1), SnmpAdminString().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, 32))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: snmpNotifyName.setDescription("The locally arbitrary, but unique identifier associated\nwith this snmpNotifyEntry.")
snmpNotifyTag = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 2), SnmpTagValue().clone('')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyTag.setDescription("This object contains a single tag value which is used\nto select entries in the snmpTargetAddrTable.  Any entry\nin the snmpTargetAddrTable which contains a tag value\nwhich is equal to the value of an instance of this\nobject is selected.  If this object contains a value\nof zero length, no entries are selected.")
snmpNotifyType = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 3), Integer().subtype(subtypeSpec=constraint.SingleValueConstraint(2,1,)).subtype(namedValues=namedval.NamedValues(("trap", 1), ("inform", 2), )).clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyType.setDescription("This object determines the type of notification to\n\n\n\nbe generated for entries in the snmpTargetAddrTable\nselected by the corresponding instance of\nsnmpNotifyTag.  This value is only used when\ngenerating notifications, and is ignored when\nusing the snmpTargetAddrTable for other purposes.\n\nIf the value of this object is trap(1), then any\nmessages generated for selected rows will contain\nUnconfirmed-Class PDUs.\n\nIf the value of this object is inform(2), then any\nmessages generated for selected rows will contain\nConfirmed-Class PDUs.\n\nNote that if an SNMP entity only supports\ngeneration of Unconfirmed-Class PDUs (and not\nConfirmed-Class PDUs), then this object may be\nread-only.")
snmpNotifyStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyStorageType.setDescription("The storage type for this conceptual row.\nConceptual rows having the value 'permanent' need not\nallow write-access to any columnar objects in the row.")
snmpNotifyRowStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 5), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyRowStatus.setDescription("The status of this conceptual row.\n\nTo create a row in this table, a manager must\nset this object to either createAndGo(4) or\ncreateAndWait(5).")
snmpNotifyFilterProfileTable = MibTable((1, 3, 6, 1, 6, 3, 13, 1, 2))
if mibBuilder.loadTexts: snmpNotifyFilterProfileTable.setDescription("This table is used to associate a notification filter\nprofile with a particular set of target parameters.")
snmpNotifyFilterProfileEntry = MibTableRow((1, 3, 6, 1, 6, 3, 13, 1, 2, 1)).setIndexNames((1, "SNMP-TARGET-MIB", "snmpTargetParamsName"))
if mibBuilder.loadTexts: snmpNotifyFilterProfileEntry.setDescription("An entry in this table indicates the name of the filter\nprofile to be used when generating notifications using\nthe corresponding entry in the snmpTargetParamsTable.\n\nEntries in the snmpNotifyFilterProfileTable are created\nand deleted using the snmpNotifyFilterProfileRowStatus\nobject.")
snmpNotifyFilterProfileName = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 1), SnmpAdminString().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, 32))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterProfileName.setDescription("The name of the filter profile to be used when generating\nnotifications using the corresponding entry in the\nsnmpTargetAddrTable.")
snmpNotifyFilterProfileStorType = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 2), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterProfileStorType.setDescription("The storage type for this conceptual row.\nConceptual rows having the value 'permanent' need not\nallow write-access to any columnar objects in the row.")
snmpNotifyFilterProfileRowStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 3), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterProfileRowStatus.setDescription("The status of this conceptual row.\n\nTo create a row in this table, a manager must\nset this object to either createAndGo(4) or\ncreateAndWait(5).\n\nUntil instances of all corresponding columns are\nappropriately configured, the value of the\ncorresponding instance of the\nsnmpNotifyFilterProfileRowStatus column is 'notReady'.\n\nIn particular, a newly created row cannot be made\nactive until the corresponding instance of\nsnmpNotifyFilterProfileName has been set.")
snmpNotifyFilterTable = MibTable((1, 3, 6, 1, 6, 3, 13, 1, 3))
if mibBuilder.loadTexts: snmpNotifyFilterTable.setDescription("The table of filter profiles.  Filter profiles are used\nto determine whether particular management targets should\nreceive particular notifications.\n\nWhen a notification is generated, it must be compared\nwith the filters associated with each management target\nwhich is configured to receive notifications, in order to\ndetermine whether it may be sent to each such management\ntarget.\n\nA more complete discussion of notification filtering\ncan be found in section 6. of [SNMP-APPL].")
snmpNotifyFilterEntry = MibTableRow((1, 3, 6, 1, 6, 3, 13, 1, 3, 1)).setIndexNames((0, "SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileName"), (1, "SNMP-NOTIFICATION-MIB", "snmpNotifyFilterSubtree"))
if mibBuilder.loadTexts: snmpNotifyFilterEntry.setDescription("An element of a filter profile.\n\nEntries in the snmpNotifyFilterTable are created and\ndeleted using the snmpNotifyFilterRowStatus object.")
snmpNotifyFilterSubtree = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 1), ObjectIdentifier()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: snmpNotifyFilterSubtree.setDescription("The MIB subtree which, when combined with the corresponding\ninstance of snmpNotifyFilterMask, defines a family of\nsubtrees which are included in or excluded from the\nfilter profile.")
snmpNotifyFilterMask = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 2), OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 16)).clone('')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterMask.setDescription("The bit mask which, in combination with the corresponding\ninstance of snmpNotifyFilterSubtree, defines a family of\nsubtrees which are included in or excluded from the\nfilter profile.\n\nEach bit of this bit mask corresponds to a\nsub-identifier of snmpNotifyFilterSubtree, with the\nmost significant bit of the i-th octet of this octet\nstring value (extended if necessary, see below)\ncorresponding to the (8*i - 7)-th sub-identifier, and\nthe least significant bit of the i-th octet of this\noctet string corresponding to the (8*i)-th\nsub-identifier, where i is in the range 1 through 16.\n\nEach bit of this bit mask specifies whether or not\nthe corresponding sub-identifiers must match when\ndetermining if an OBJECT IDENTIFIER matches this\nfamily of filter subtrees; a '1' indicates that an\nexact match must occur; a '0' indicates 'wild card',\ni.e., any sub-identifier value matches.\n\n\n\nThus, the OBJECT IDENTIFIER X of an object instance\nis contained in a family of filter subtrees if, for\neach sub-identifier of the value of\nsnmpNotifyFilterSubtree, either:\n\n  the i-th bit of snmpNotifyFilterMask is 0, or\n\n  the i-th sub-identifier of X is equal to the i-th\n  sub-identifier of the value of\n  snmpNotifyFilterSubtree.\n\nIf the value of this bit mask is M bits long and\nthere are more than M sub-identifiers in the\ncorresponding instance of snmpNotifyFilterSubtree,\nthen the bit mask is extended with 1's to be the\nrequired length.\n\nNote that when the value of this object is the\nzero-length string, this extension rule results in\na mask of all-1's being used (i.e., no 'wild card'),\nand the family of filter subtrees is the one\nsubtree uniquely identified by the corresponding\ninstance of snmpNotifyFilterSubtree.")
snmpNotifyFilterType = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 3), Integer().subtype(subtypeSpec=constraint.SingleValueConstraint(1,2,)).subtype(namedValues=namedval.NamedValues(("included", 1), ("excluded", 2), )).clone(1)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterType.setDescription("This object indicates whether the family of filter subtrees\ndefined by this entry are included in or excluded from a\nfilter.  A more detailed discussion of the use of this\nobject can be found in section 6. of [SNMP-APPL].")
snmpNotifyFilterStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterStorageType.setDescription("The storage type for this conceptual row.\nConceptual rows having the value 'permanent' need not\n\n\n\nallow write-access to any columnar objects in the row.")
snmpNotifyFilterRowStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 5), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpNotifyFilterRowStatus.setDescription("The status of this conceptual row.\n\nTo create a row in this table, a manager must\nset this object to either createAndGo(4) or\ncreateAndWait(5).")
snmpNotifyConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3))
snmpNotifyCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3, 1))
snmpNotifyGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3, 2))

# Augmentions

# Groups

snmpNotifyFilterGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 13, 3, 2, 2)).setObjects(("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterRowStatus"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileStorType"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileName"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterType"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterStorageType"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterMask"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileRowStatus"), )
snmpNotifyGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 13, 3, 2, 1)).setObjects(("SNMP-NOTIFICATION-MIB", "snmpNotifyTag"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyRowStatus"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyStorageType"), ("SNMP-NOTIFICATION-MIB", "snmpNotifyType"), )

# Exports

# Module identity
mibBuilder.exportSymbols("SNMP-NOTIFICATION-MIB", PYSNMP_MODULE_ID=snmpNotificationMIB)

# Objects
mibBuilder.exportSymbols("SNMP-NOTIFICATION-MIB", snmpNotificationMIB=snmpNotificationMIB, snmpNotifyObjects=snmpNotifyObjects, snmpNotifyTable=snmpNotifyTable, snmpNotifyEntry=snmpNotifyEntry, snmpNotifyName=snmpNotifyName, snmpNotifyTag=snmpNotifyTag, snmpNotifyType=snmpNotifyType, snmpNotifyStorageType=snmpNotifyStorageType, snmpNotifyRowStatus=snmpNotifyRowStatus, snmpNotifyFilterProfileTable=snmpNotifyFilterProfileTable, snmpNotifyFilterProfileEntry=snmpNotifyFilterProfileEntry, snmpNotifyFilterProfileName=snmpNotifyFilterProfileName, snmpNotifyFilterProfileStorType=snmpNotifyFilterProfileStorType, snmpNotifyFilterProfileRowStatus=snmpNotifyFilterProfileRowStatus, snmpNotifyFilterTable=snmpNotifyFilterTable, snmpNotifyFilterEntry=snmpNotifyFilterEntry, snmpNotifyFilterSubtree=snmpNotifyFilterSubtree, snmpNotifyFilterMask=snmpNotifyFilterMask, snmpNotifyFilterType=snmpNotifyFilterType, snmpNotifyFilterStorageType=snmpNotifyFilterStorageType, snmpNotifyFilterRowStatus=snmpNotifyFilterRowStatus, snmpNotifyConformance=snmpNotifyConformance, snmpNotifyCompliances=snmpNotifyCompliances, snmpNotifyGroups=snmpNotifyGroups)

# Groups
mibBuilder.exportSymbols("SNMP-NOTIFICATION-MIB", snmpNotifyFilterGroup=snmpNotifyFilterGroup, snmpNotifyGroup=snmpNotifyGroup)
