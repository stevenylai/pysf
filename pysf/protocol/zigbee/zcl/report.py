'''ZCL attribute report'''


class ReportConfig:
    ZCL_SEND_ATTR_REPORTS = 0
    ZCL_EXPECT_ATTR_REPORTS = 1

    direction = 0
    attr_id = 0
    type = 0
    min_interval = 0
    max_interval = 0
    timeout = 0
    threshold = b''
