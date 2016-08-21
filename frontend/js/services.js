/**
 * Created by guoli on 16-2-25.
 */

/*Services*/

var musicServices = angular.module('musicServices',['ngResource']);

musicServices.factory('MusicGet',['$resource',
    function($resource) {

        return $resource("http://172.21.213.119/get",{},{
            get: {method: 'GET', cache: false, isArray: false},
            save: {method: 'POST', cache: false, isArray: true}
        });
    }
]);

musicServices.factory('ResGet',['$resource',
    function($resource) {

        // return $resource(apiurl + "list",{},{

        //setting url params
        return $resource(apiurl + ":verb",{},{
            get: {method: 'GET', cache: false, isArray: true},
            save: {method: 'POST', cache: false, isArray: true}
        });
    }
]);

musicServices.factory('SongGet',['$resource',
    function($resource) {

        return $resource( apiurl + "meta",{},{
            get: {method: 'GET', cache: false, isArray: false},
            save: {method: 'POST', cache: false, isArray: false}
        });
    }
]);

musicServices.factory('AlbumGet',['$resource',
    function ($resource) {

        return $resource('/frontend/resources/album',{},{
            get: {method: 'GET', cache: false, isArray: true},
            save: {method: 'POST', cache: false, isArray: true}
        });
    }
]);

musicServices.factory('RcdGet',['$resource',
    function ($resource) {

        return $resource(apiurl + "recommendation",{},{
            get: {method: 'GET', cache: false, isArray: true},
            save: {method: 'POST', cache: false, isArray: true}
        });
    }
]);

// data share, note data bind from service about watch, digest, apply same as scope.
musicServices.factory('DataShare', function () {
    return {
        model: 'now',
        trick: {verb :'list'},
        list: []
    };

});
