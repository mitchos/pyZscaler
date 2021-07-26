import time

from pyzscaler.zia import ZIA

with ZIA() as zia:
    complete = False
    zia.audit_logs.create(start_time="1627221600000", end_time="1627271676622")

    while not complete:
        if zia.audit_logs.status().status == "COMPLETE":
            complete = True
        time.sleep(2)  # 2 seconds is enough to avoid API limits

    with open("audit_log.csv", "w+") as fh:
        fh.write(zia.audit_logs.get_report())
