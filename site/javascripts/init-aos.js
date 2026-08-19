document.addEventListener("DOMContentLoaded", function() {
    AOS.init({
        duration: 800, // 动画持续时间（毫秒）
        easing: 'ease-out-cubic', // 动画缓冲函数，让动画更平滑
        once: true, // 是否只执行一次动画，不建议来回划都触发
        offset: 80, // 距离触发点多少像素时触发动画
        delay: 50 // 统一稍微延迟一下，增加优雅感
    });
});
