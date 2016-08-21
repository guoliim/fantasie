/**
 * Created by guoli on 16-2-22.
 */
/*Music Radio App*/

var musicRadioApp = angular.module('musicRadioApp',[
    'ngRoute',
    'musicServices',
    'musicPlayerControllers',
    'albumControllers'
]);

musicRadioApp.config(['$routeProvider', '$locationProvider',
    function ($routerProvider, $locationProvider) {
        $routerProvider
            .when('/fantasie/:state',{
                templateUrl: '/frontend/partials/fantasie.html',
                controller: 'Recommendation'
            })
            .when('/fantasie/:play/:content',{
                templateUrl: '/frontend/partials/music_content.html',
                controller: 'Content'
            })
            .when('/list',{
                templateUrl: '/frontend/partials/album_list.html',
                controller: 'AlbumsList'
            })

            // Sets default page, $routeParams = fantasie;
            .otherwise({
            //Sets route definition that will be used on route change when no other route definition is matched.
            redirectTo: '/fantasie/now'
        });

        //easily support SEO
        // $locationProvider.hashPrefix('!');

        // $locationProvider.html5Mode(true);

        // $locationProvider.html5Mode({
        //     enabled: true,
        //     requireBase: false
        // });
    }]);
