// Hides the password, password confirmation and password-based
// authentication rows on the admin add-user form while the
// "Autogenerate password" checkbox is checked.
//
// Media scripts are rendered in <head> (unfold change_form extrahead), so
// the checkbox does not exist yet at parse time — wait for DOMContentLoaded.
document.addEventListener("DOMContentLoaded", function () {
  var checkbox = document.querySelector('input[name="autogenerate_password"]');
  if (!checkbox) {
    return;
  }

  var fieldIds = ["id_password1", "id_password2", "id_usable_password"];

  function toggle() {
    var hidden = checkbox.checked;
    fieldIds.forEach(function (id) {
      var input = document.getElementById(id);
      var row = input ? input.closest(".field-line") : null;
      if (row) {
        row.style.display = hidden ? "none" : "";
      }
    });
  }

  checkbox.addEventListener("change", toggle);
  toggle();
});
