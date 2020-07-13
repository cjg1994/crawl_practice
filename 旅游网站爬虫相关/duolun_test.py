import execjs
s="""var _1s = function () {
    setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')', 1500);
    return  '__jsl_clearance=1580790940.655|0|' + (function () {
        return ['h', ((+!{}) + [
            []
        ][0]), 'Y', ((+!~~{}) - ~(+!~~{}) + [] + []) + ((+!~~{}) / (+[]) + []).charAt(~~'') + (!'' + [
            []
        ][0]).charAt(-~(+!{})), 'zB', [(-~(+!~~{})) * [(-~(+!~~{}) << (+!~~{}))]] + (-~(+!{}) + [
            []
        ][0]) + [{} + [
            []
        ][0]][0].charAt((+!~~{})), 'mW', ((+!~~{}) / (+[]) + []).charAt(~~''), 'k', (!!!window.headless + [] + [
            []
        ][0]).charAt(2) + [window.headless + [] + [
            []
        ][0]][0].charAt(-~(+!{})) + ({} + [] + []).charAt(((+!~~{}) << (+!~~{}))) + ({} + [] + []).charAt(((+!~~{}) << (+!~~{}))) + (![] + [] + [
            []
        ][0]).charAt((-~[] | 2)), 'Z', [2], 'mP', (!'' + [
            []
        ][0]).charAt(-~(+!{})) + (-~(4) + []) + [(-~(+!~~{})) * [(-~(+!~~{}) << (+!~~{}))]], '%', ((+!~~{}) - ~(+!~~{}) + [] + []), 'D'].join('')
    })() + ';Expires=Tue, 04-Feb-20 05:35:40 GMT;Path=/;'
};
if ((function () {
    try {
        return !!window.addEventListener;
    } catch (e) {
        return false;
    }
})()) {
    document.addEventListener('DOMContentLoaded', _1s, false)
} else {
    document.attachEvent('onreadystatechange', _1s)
}"""
content=execjs.compile(s)
d=content.call('_1s')
print(d)
