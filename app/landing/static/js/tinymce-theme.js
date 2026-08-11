/* Adapt django-tinymce editors to the Unfold light/dark admin theme.
 *
 * Unfold toggles dark mode by adding/removing the `dark` class on <html>.
 * TinyMCE can't switch skins at runtime on its own, so we:
 *   1. Inject the correct `skin` / `content_css` into each textarea's
 *      data-mce-conf BEFORE django-tinymce's init script runs.
 *   2. Watch the <html> class for theme changes and rebuild every editor
 *      with the matching skin (content is flushed first so nothing is lost).
 */
(function () {
  "use strict";

  function isDark() {
    return document.documentElement.classList.contains("dark");
  }

  function skinForTheme() {
    return isDark() ? "oxide-dark" : "oxide";
  }

  function contentCssForTheme() {
    return isDark() ? "dark" : "default";
  }

  // Rewrite a textarea's data-mce-conf so the next editor init uses the
  // skin that matches the current Unfold theme.
  function patchTextarea(textarea) {
    if (!textarea || !textarea.dataset || !textarea.dataset.mceConf) {
      return;
    }
    try {
      var conf = JSON.parse(textarea.dataset.mceConf);
      conf.skin = skinForTheme();
      conf.content_css = contentCssForTheme();
      textarea.dataset.mceConf = JSON.stringify(conf);
    } catch (err) {
      /* leave untouched if the config cannot be parsed */
    }
  }

  function patchAll() {
    var areas = document.querySelectorAll("textarea.tinymce");
    for (var i = 0; i < areas.length; i++) {
      patchTextarea(areas[i]);
    }
  }

  // Rebuild every editor with the skin for the current theme. Content is
  // flushed to the textarea first so nothing is lost.
  function reapplyTheme() {
    if (!window.tinyMCE) {
      return;
    }
    var areas = document.querySelectorAll("textarea.tinymce");
    for (var i = 0; i < areas.length; i++) {
      var textarea = areas[i];
      var editor = window.tinyMCE.get(textarea.id);
      if (!editor) {
        continue;
      }
      editor.save();
      editor.remove();
      patchTextarea(textarea);
      if (!window.tinyMCE.get(textarea.id)) {
        try {
          window.tinyMCE.init(JSON.parse(textarea.dataset.mceConf));
        } catch (err) {
          /* ignore */
        }
      }
    }
  }

  function boot() {
    // This listener is registered before django-tinymce's own
    // DOMContentLoaded listener (our script is injected earlier in <head>),
    // so editors are initialized with the theme-matched config.
    patchAll();

    // Patch new inline editors added through the Django admin.
    if (window.django && window.django.jQuery) {
      window.django.jQuery(document).on("formset:added", function (event, $row) {
        var scope = event.detail && event.detail.formsetName
          ? event.target
          : $row.get(0);
        var areas = (scope || document).querySelectorAll("textarea.tinymce");
        for (var i = 0; i < areas.length; i++) {
          patchTextarea(areas[i]);
        }
      });
    }

    // Rebuild editors when Unfold toggles the `.dark` class on <html>.
    if ("MutationObserver" in window) {
      var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          if (
            mutations[i].type === "attributes" &&
            mutations[i].attributeName === "class"
          ) {
            reapplyTheme();
            break;
          }
        }
      });
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }
  }

  if (document.readyState !== "loading") {
    boot();
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
