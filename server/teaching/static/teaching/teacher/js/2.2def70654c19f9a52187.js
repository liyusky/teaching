webpackJsonp([2],{EV1k:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i=s("BRoD"),n=s("LvBe"),a=s("Zbsp"),o=s("DQny"),r=s("H9my"),m=s("kA2o"),c={name:"LoginComponent",data:function(){return{mode:!1,phone:"",password:"",imageCode:"",smsCode:"",modeBtnText:"手机验证码登录",sendSMSBtnText:"获取验证码",codeImage:a.a.baseUrl+"/common/image-code?time="+new Date,submitDisabled:!1,smsDisabled:!1}},components:{},created:function(){this.clearStorage(),this.getCodeImage()},mounted:function(){this.getCodeImage()},methods:{changMode:function(){this.mode=!this.mode,this.modeBtnText=this.mode?"密码登录":"手机验证码登录"},submit:function(){this.mode?this.loginBySMS():this.loginByPassword(),this.getCodeImage()},loginByPassword:function(){var e=this;n.a.account(this.phone)&&n.a.password(this.password)&&n.a.imageCode(this.imageCode)&&(this.submitDisabled=!0,r.a.send({url:"LoginByPassword",data:{phone:this.phone,password:this.password,imageCode:this.imageCode}}).success(function(e){i.a.info=e,i.a.role?(m.a.push("manager-class"),e.name||(o.a.panel="user-update-user")):alert("您不是教师，无法登陆")}).fail(function(e){}).default(function(){e.submitDisabled=!1}))},loginBySMS:function(){var e=this;n.a.phone(this.phone)&&n.a.smsCode(this.smsCode)&&(this.submitDisabled=!0,r.a.send({url:"LoginBySMS",data:{phone:this.phone,smsCode:this.smsCode}}).success(function(e){i.a.info=e,i.a.role?(m.a.push("manager-class"),e.name||(o.a.panel="user-update-user")):alert("您不是教师，无法登陆")}).fail(function(e){console.log(e)}).default(function(){e.submitDisabled=!1}))},getCodeImage:function(){this.codeImage=window.baseUrl+"/common/image-code?time="+new Date},sendSMSCaptcha:function(){var e=this;n.a.phone(this.phone)&&n.a.imageCode(this.imageCode)&&(this.waitOneMinute(),r.a.send({url:"SMSCaptcha",data:{phone:this.phone,imageCode:this.imageCode,scene:0}}).success(function(e){alert("短信验证码发送成功")}).fail(function(e){}).default(function(){e.getCodeImage()}))},waitOneMinute:function(){var e=this;this.smsDisabled=!0,this.sendSMSBtnText="60秒后重发";var t=60,s=setInterval(function(){--t>0?e.sendSMSBtnText=t+"秒后重发":(e.sendSMSBtnText="获取短信验证码",clearInterval(s),e.smsDisabled=!1)},1e3)},clearStorage:function(){this.$store.commit("account",{}),this.$store.commit("origin",null),this.$store.commit("modal",!1),this.$store.commit("panel",!1),this.$store.commit("detail",!1),this.$store.commit("api",!1),this.$store.commit("tip",!1),this.$store.commit("content",!1),this.$store.commit("communication",{}),this.$store.commit("menu",""),localStorage.clear()}}},l={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("section",{staticClass:"login"},[e._m(0),e._v(" "),s("div",{staticClass:"login-area"},[e._m(1),e._v(" "),s("ul",{staticClass:"area-input-list"},[s("li",{staticClass:"list-item border-1"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.phone,expression:"phone"}],staticClass:"item-input",attrs:{type:"text",maxlength:"11",placeholder:"请输入手机号"},domProps:{value:e.phone},on:{keyup:[function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.submit(t):null},function(t){return("button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter"))&&t.ctrlKey?e.sendSMSCaptcha(t):null}],input:function(t){t.target.composing||(e.phone=t.target.value)}}})]),e._v(" "),s("li",{directives:[{name:"show",rawName:"v-show",value:!e.mode,expression:"!mode"}],staticClass:"list-item border-1"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"item-input",attrs:{type:"password",maxlength:"20",placeholder:"请输入密码"},domProps:{value:e.password},on:{keyup:function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.submit(t):null},input:function(t){t.target.composing||(e.password=t.target.value)}}})]),e._v(" "),s("li",{staticClass:"list-item border-1"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.imageCode,expression:"imageCode"}],staticClass:"item-input",attrs:{type:"text",maxlength:"4",placeholder:"请输入图形验证码"},domProps:{value:e.imageCode},on:{keyup:[function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.submit(t):null},function(t){return("button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter"))&&t.ctrlKey?e.sendSMSCaptcha(t):null}],input:function(t){t.target.composing||(e.imageCode=t.target.value)}}}),e._v(" "),s("img",{staticClass:"item-image",attrs:{src:e.codeImage},on:{click:e.getCodeImage}})]),e._v(" "),s("li",{directives:[{name:"show",rawName:"v-show",value:e.mode,expression:"mode"}],staticClass:"list-item border-1"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.smsCode,expression:"smsCode"}],staticClass:"item-input",attrs:{type:"text",maxlength:"6",placeholder:"请输入短信验证码"},domProps:{value:e.smsCode},on:{keyup:[function(t){return"button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter")?e.submit(t):null},function(t){return("button"in t||!e._k(t.keyCode,"enter",13,t.key,"Enter"))&&t.ctrlKey?e.sendSMSCaptcha(t):null}],input:function(t){t.target.composing||(e.smsCode=t.target.value)}}}),e._v(" "),s("button",{staticClass:"item-btn",attrs:{disabled:e.smsDisabled},on:{click:e.sendSMSCaptcha}},[e._v(e._s(e.sendSMSBtnText))])])]),e._v(" "),s("button",{staticClass:"area-btn",attrs:{disabled:e.submitDisabled},on:{click:e.submit}},[s("div",[e._v("登录")])]),e._v(" "),s("div",{staticClass:"area-mode"},[s("button",{on:{click:e.changMode}},[e._v(e._s(e.modeBtnText))])])])])},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"login-background"},[t("img",{attrs:{src:s("ctKR")}})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"area-logo"},[t("img",{staticClass:"logo-image",attrs:{src:s("Z2Ou")}}),this._v(" "),t("p",{staticClass:"logo-tip"},[this._v("发现编程的乐趣")])])}]};var d=s("VU/8")(c,l,!1,function(e){s("Griu")},"data-v-02f516bb",null);t.default=d.exports},Griu:function(e,t){},Z2Ou:function(e,t,s){e.exports=s.p+"teacher/img/logo.8f4c159.png"},ctKR:function(e,t,s){e.exports=s.p+"teacher/img/bg.dcfa866.jpg"}});