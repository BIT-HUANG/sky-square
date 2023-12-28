class BaseConfig:
    JIRA_URL = "https://jira.skycoresaas.com/"
    CONFLUENCE_URL = "https://confluence.skycoresaas.com/"
    JENKINS_URL = "https://nonprod-jenkins.skycoresaas.com/"
    USERNAME = "huanghongxiang@skycoresaas.com"
    ATLAS_PASSWORD = "123456"
    JENKINS_PASSWORD = "11b853505f754a137e02862bc655f3039f"
    QA_JENKINS_URL = "https://test-jenkins.skycoresaas.com"
    QA_JENKINS_USERNAME = "huanghongxiang"
    QA_JENKINS_PASSWORD = "11167898e32bc9aaea9547645ebc1bc029"


class SkyCoreService:
    SKYCORE_SERVICE_DICT = {
        'resource_svc': '',
        'ram-mo': '',
        'identity-svc': '',
        'pms-mo': '',
        'payment-svc': '',
        'nbcb-gw': '',
        'process-svc': '',
        'pdm-mo': '',
        'material-svc': '',
        'material-public-svc': '',
        'wechatpay-gw': '',
        'shop-svc': '',
        'product-svc': '',
        'order-svc': '',
        'oms-mo': '',
        'alipay-gw': '',
        'kingdee-gw': '',
        'esign-gw': '',
        'front-end_uni-mall': '',
        'front-end_static': '',
        'front-end_ssr-vue': '',
        'front-end_others_user-agreement': '',
        'front-end_oms': '',
        'front-end_CIMP': '',
        'es_elasticsearch-agt': '',
        'marketing-svc': '',
        'customer-svc': '',
        'crm-mo': '',
        'sms-gw': '',
        'qcc-gw': '',
        'fs-svc': '',
        'common-svc': '',
        'common-mo': '',
        'camunda-svc': '',
        'bpm-mo': '',
        'open-api': '',
        'old_skycore-office-fe': '',
        'old-pdm-ret-svc': '',
        'sc-scripts': '',
        'spring-cloud-gateway': '',
        'spring-boot-admin': ''
    }
