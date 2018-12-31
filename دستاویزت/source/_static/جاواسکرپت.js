function myFunction() {
  var h1 = document.documentElement;
  var att = document.createAttribute("dir");
  att.value = "rtl";
  h1.setAttributeNode(att);
}
