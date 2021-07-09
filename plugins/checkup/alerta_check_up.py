import datetime
import logging
from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins')


class CheckUp(PluginBase):
    """
    Add "anomaly" attribute to alerts
    to check the status is error or ok
    """

    def pre_receive(self, alert, **kwargs):
        # 判断是否健康
        anomaly = False
        # 1. 判断当天是否有多于一条数据
        alertQ = alert()
        alertQ.customer = alert.customer
        records = alert.get_alert_history(alertQ)
        count7 = 0
        count30 = 0
        for record in records:
            updateTime = datetime.datetime.strptime('%Y-%m-%d', record.update_time)

            # 判断一天的
            now = datetime.datetime.now().strptime('%Y-%m-%d')
            if updateTime == now:
                anomaly = True

            # 2 判断一周七天是否有多于7条数据
            monday = self.this_monday()
            if monday <= updateTime <= now:
                count7 += 1
                if count7 > 7:
                    anomaly = True

            # 3  判断一个月是否有多于30条
            month_start = self.this_month_start()
            if month_start <= updateTime <= now:
                count30 += 1
                if count30 > 30:
                    anomaly = True
        # 更新attributes中anomaly字段
        alert.attributes['anomaly'] = anomaly
        return alert

    def post_receive(self, alert, **kwargs):
        return

    def status_change(self, alert, status, text, **kwargs):
        return

    def take_action(self, alert, action, text, **kwargs):
        return

    def delete(self, alert, **kwargs) -> bool:
        raise NotImplementedError

    def this_monday(self):
        """
        :function: 获取本周周一日期
        :return: 返回周一的日期
        :return_type: string
        """
        today = datetime.datetime.now().strptime('%Y-%m-%d')
        return datetime.strftime(today - datetime.timedelta(today.weekday()), '%Y-%m-%d')

    def this_month_start(self):
        """
        :function: 获取本月第一天
        :return: 返回本月第一天
        :return_type: string
        """
        today = datetime.datetime.now()
        this_month_start = datetime.datetime(today.year, today.month, 1)
        return datetime.strftime(this_month_start, '%Y-%m-%d')
