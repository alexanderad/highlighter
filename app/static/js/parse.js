$(function() {
  var url = decodeURIComponent(window.location.href.split("?u=")[1]);
  $.post("/v1/parse", { url: url }, function(response) {
    if (response.success) {
      window.location.replace("/read?t=" + response.page_id);
    } else {
      window.location.replace("/?error=" + response.error);
    }
  });
});
