function valid_username(str) {
  var re= /[\w\_]{4,12}/;
  return re.test(str);
}

function valid_password(str) {
  var len = str.length;
  return len >= 6 && len <= 18;
}

function valid_student_id(str) {
  var re = /\d{8}/;
  return re.test(str);
}

function not_blank(str) {
  return $.trim(str) != ''
}

function mySignUp() {
  var my_form = $('.my-form-signup input');
  var warn = $('#signup-form-warning');
  var valid = true;

  if (!valid_username(my_form.eq(0).val())) {
    warn.text('用户名需要以字母，数字，下划线组成，长度4-12');
    valid = false;
  } else if (!not_blank(my_form.eq(1).val()) ) {
    warn.text('昵称不能为空');
    valid = false;
  } else if (!valid_password(my_form.eq(2).val())) {
    warn.text('密码格式错误，密码长度需为6-18位');
    valid = false;
  } else if (!valid_student_id(my_form.eq(3).val())) {
    warn.text('学号应为8位数字');
    valid = false;
  } else if (!not_blank(my_form.eq(4).val()) ) {
    warn.text('姓名不能为空');
    valid = false;
  } else if ($('#user-contact-type').val() == '') {
    warn.text('请选择联系方式类型');
    valid = false;
  } else if (!not_blank(my_form.eq(5).val()) ) {
    warn.text('联系方式不能为空');
    valid = false;
  }

  if (!valid) {
    warn.show();
    return false;
  }

  var jsxhr = $.post('/ajax_register', {
    username: my_form.eq(0).val(),
    nickname: my_form.eq(1).val(),
    password: my_form.eq(2).val(),
    student_id: my_form.eq(3).val(),
    student_name: my_form.eq(4).val(),
    contact_type: $('#user-contact-type').val(),
    contact_way: my_form.eq(5).val()
  }).done(function (data) {
    if (data.result == 1) {
      warn.text('用户名已存在');
    } else if (data.result == -1) {
      warn.text('未知错误,请联系管理员');
    } else {
      window.location.reload();
    }
  }).fail(function (xhs, status){
    warn.text('失败: ' + xhr.status + '\n原因: ', status);
  });
  warn.show();
}

function myLogin() {
  var my_form = $('.my-form-login input');
  var warn = $('#login-form-warning');
  var valid = true;

  if (!valid_username(my_form.eq(0).val())) {
    warn.text('用户名格式错误');
    valid = false;
  } else if (!valid_password(my_form.eq(1).val())) {
    warn.text('密码格式错误，密码长度需为6-18位');
    valid = false;
  }
  if (!valid) {
    warn.show();
    return false;
  }

  var jsxhr = $.post('/ajax_login', {
    username: my_form.eq(0).val(),
    password: my_form.eq(1).val()
  }).done(function (data) {
    if (data.result != 0) {
      warn.text("用户名或密码错误");
    } else {
      window.location.reload();
    }
  }).fail(function (xhr, status){
    warn.text('失败: ' + xhr.status + '\n原因: ', status);
  });
  warn.show();
}

function myLogout() {
  var jsxhr = $.post('/ajax_logout', {}).done(function(data){
    if (data.result == 0) {
      window.location.reload();
    }
  });
}

function newPickSubmit() {
  var form = $('#new-record-form');

  if ($('#new-pick-type').val() == '') {
    alert("请选择失物类型");
    return false;
  }
  if ($('#new-pick-contact-type').val() == '') {
    alert("请选择联系方式类型");
    return false;
  }

  form.submit();
}

function newLostSubmit() {
  var form = $('#new-record-form');

  if ($('#new-pick-type').val() == '') {
    alert("请选择失物类型");
    return false;
  }
  if ($('#new-pick-contact-type').val() == '') {
    alert("请选择联系方式类型");
    return false;
  }

  form.submit();
}

function updateForm(lst) {
  var sec = $('div.section');
  sec.hide();
  for (var i = 0; i < lst.length; i++) {
    var blk = sec.eq(i);
    blk.show();
    blk.find('label').text(lst[i]);
    blk.find('input').val('');
  }
}

function newRecordTypeChange() {
  var slt = $("#new-record-type");
  var lst = [];
  if (slt.val() == '') {
    lst = [];
  } else if (slt.val() == 'student card') {
    lst = ['学号', '姓名', '地点'];
  } else if (slt.val() == 'credit card') {
    lst = ['所属银行', '尾号(后4位)', '地点'];
  } else if (slt.val() == 'else') {
    lst = ['类型', '地点', '时间'];
  }
  updateForm(lst);
}

function uploadSelected() {
  var obj = $('#picture').prev();
  var str = $('#picture').val().split('\\').slice(-1);
  if (str == '') {
    str = '选择图片...';
  } else {
    str = '选中' + str;
  }
  obj.text(str);
}
