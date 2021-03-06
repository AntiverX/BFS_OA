/*jshint esversion: 6 */


Vue.component('index',{
    template : `
        <el-row type="flex" class="row-bg" justify="center">
            <el-col :span="12">
                <div class="grid-content">
                    <el-alert type="success" :closable="false">
<!--                        {% if have_uploaded == 1 %}-->
<!--                            课题管理表上次更新时间：{{ last_update_time|date:"Y-m-d H:i" }}-->
<!--                        {% else %}-->
<!--                            {{ last_update_time }}-->
<!--                        {% endif %}-->
                    </el-alert>

                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span>上传文件</span>
                        </div>
<!--                        {% csrf_token %}-->
                        <el-form ref="form" label-width="80px">
                            <el-upload
                                    class="upload-demo"
                                    action=""
                                    :data="message"
                                    :on-success="test"
                                    :file-list="fileList">
                                <el-button size="small" type="primary">点击上传</el-button>
                                <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
                            </el-upload>
                        </el-form>

                    </el-card>
                </div>
            </el-col>
        </el-row>
    `,
    methods : {

        test() {
            "use strict";
            alert("上传成功");
            },
    },
    data () {
        "use strict";
        return {
            message : {'csrfmiddlewaretoken': this.csrf_token },
        }
    },
    props: ['csrf_token'],
});