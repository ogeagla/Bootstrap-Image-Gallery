/*
 * Bootstrap Image Gallery JS Demo 3.0.0
 * https://github.com/blueimp/Bootstrap-Image-Gallery
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint unparam: true */
/*global window, document, blueimp, $ */

$(function () {
    'use strict';

    
    var linksContainer = $('#links');
    var photos = [
        {


//need to rotate them and actually make these point to the thumbnails but link to the high res version
            "url":"img/test1.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0262.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0318.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0335.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0359.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0371.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0372.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0387.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0403.jpg",
            "title":"test1"
        },
        {
            "url":"img/IMG_0406.jpg",
            "title":"test1"
        }
    ];
    // Add the demo images as links with thumbnails to the page:
    for(var index = 0; index < photos.length; index++) {
        var photo = photos[index];
        $('<a/>')
            .append($('<img>').prop('src', photo.url))
            .prop('href', photo.url)
            .prop('title', photo.title)
            .attr('data-gallery', '')
            .appendTo(linksContainer);
    }
    
    $('#borderless-checkbox').on('change', function () {
        var borderless = $(this).is(':checked');
        $('#blueimp-gallery').data('useBootstrapModal', !borderless);
        $('#blueimp-gallery').toggleClass('blueimp-gallery-controls', borderless);
    });

    $('#fullscreen-checkbox').on('change', function () {
        $('#blueimp-gallery').data('fullScreen', $(this).is(':checked'));
    });

    $('#image-gallery-button').on('click', function (event) {
        event.preventDefault();
        blueimp.Gallery($('#links a'), $('#blueimp-gallery').data());
    });

});
