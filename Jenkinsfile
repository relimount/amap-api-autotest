// amap-api-test 的流水线定义

pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'AMAP_QPS', defaultValue: '2.5',
               description: '限流速率。实测3以上会偶发CUQPS_HAS_EXCEEDED_THE_LIMIT')
    }

    triggers {
        cron('0 8 * * *')
    }

    environment {
        AMAP_KEY = credentials('amap-api-key')
        AMAP_QPS = "${params.AMAP_QPS}"
        PYTHONIOENCODING = 'utf-8'
        PYTHONUTF8 = '1'
    }

    stages {
        stage('执行用例') {
            steps {
                bat '''
                    chcp 65001 > nul
                    uv run pytest -q --alluredir=report --clean-alluredir
                    '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jUnit: '', results: [[path: 'report']]
            archiveArtifacts artifacts: 'report/**', allowEmptyArchive: true
        }
        failure {
            emailext(
                to: 'relimount@163.com',
                subject: "[FAILED] ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """构建失败。

                       构建页：${env.BUILD_URL}
                       Allure：${env.BUILD_URL}allure
                       """
            )
        }
    }
}
