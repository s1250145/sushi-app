// after uploading image
document.addEventListener("DOMContentLoaded", function() {
  var input = document.querySelector('input');
  var form = document.querySelector('.up-form');
  var send = document.querySelector('.cp_btn');
  var loader = document.getElementById('loader-bg');

  input.addEventListener('change', checkInput);

  function checkInput() {
    var image = input.file;
    if(image != 0) {
      send.addEventListener('click', showLoading);

      function showLoading() {
        var list = ["アガリ：お茶のこと",
                    "ムラサキ：お醤油のこと",
                    "なみだ：わさびのこと",
                    "回らないお寿司はお箸で食べても手で食べてもよい",
                    "「すし」は中国生まれ。明時代に消滅",
                    "寿司という表記は江戸っ子が命名した当て字",
                    "江戸時代のお寿司はファーストフード",
                    "江戸時代の大阪ではお寿司はマイナー",
                    "フッターは山葵色（#a8bf93）",
                    "生わさびは辛くない"]
        loader.style.display = 'block';
        loader.style.background = '#fff';
        loader.insertAdjacentHTML('beforeend', '<p id="mame">'+ list[Math.floor(Math.random()*10)] +'</p>');
      }
    }
  }
}, false);

window.onload = function() {
  var loader = document.getElementById('loader-bg');
  loader.style.display = 'none';
  if(document.getElementById('js-popup') != null) {
    var popup = document.getElementById('js-popup');
    if(!popup) return;
    popup.classList.add('is-show');

    var blackBg = document.getElementById('js-black-bg');
    var closeBtn = document.getElementById('js-close-btn');

    closePopUp(blackBg);
    closePopUp(closeBtn);

    function closePopUp(elem) {
      if(!elem) return;
      elem.addEventListener('click', function() {
        popup.classList.remove('is-show');
      })
    }
  }
}
