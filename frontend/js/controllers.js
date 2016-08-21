/**
 * Created by guoli on 16-2-25.
 */

var musicPlayerControllers = angular.module('musicPlayerControllers',[]);
var list = [];
var init = 0;
var ua = navigator.userAgent;
var isSafari = true;

if (ua.indexOf("Chrome") != -1) {
    isSafari = false;
}

musicPlayerControllers.controller('MusicPlayer',[
    '$rootScope','$scope','ResGet','$window','SongGet','$interval','$routeParams','AlbumGet','DataShare',

    function MusicPlayer($rootScope,$scope,ResGet,$window,SongGet,$interval,$routeParams,AlbumGet,DataShare) {

        // console.log($routeParams);
        //
        // console.log("Model:" + DataShare.model);

        if ( DataShare.model === "now"){
            $scope.switch = 'now';
            console.log($scope.switch);
        } else {
            $scope.switch = 'play/content';
            console.log($scope.switch);
        }


        $scope.$on('listChange',function () {
            console.log(DataShare.model);
            if (list.length <= 1) {
                if ( DataShare.model === "now") {
                    // console.log(isSafari);
                    ResGet.get({verb: 'list', codec: 'aac'},
                        function success (response) {
                            console.log("SU:" + JSON.stringify(response));
                            $scope.res = response;
                            $scope.$emit('resChange');
                            $scope.$broadcast('resChange');
                        },
                        function error (response) {
                            console.log("Error:" + response);
                        }
                    );
                } else if ( DataShare.model !== 'now') {
                    // console.log(DataShare.trick);
                    ResGet.get(DataShare.trick,
                        function success (response) {
                            // console.log(DataShare.trick);
                            $scope.res = response;
                            $scope.$emit('resChange');
                            $scope.$broadcast('resChange');
                        },
                        function error (response) {
                            console.log("Error:" + response);
                        }
                    );
                } else {
                    $scope.songs = [];
                    AlbumGet.get(function success (response) {
                        // console.log('Success :' + JSON.stringify(response));
                        $scope.songs = response;
                        // console.log('SONGS:' + $scope.songs);
                    }, function error (response) {
                        // console.log('Error:' + response);
                    });
                }
            }
        });

        $scope.$on('resChange', function () {
            var successed = true;
            while ($scope.res.length > 0 && successed === true) {
                var node = undefined;
                SongGet.get({"rawhash":(node = $scope.res.shift()).rawhash,"safari":isSafari},
                    function success (response) {
                        successed = true;
                        // console.log(successed);
                        list.push(response);
                        if (init === 0) {
                            $scope.$emit('loadRst');
                            init = 1;
                        }
                    },
                    function error (response) {
                        successed = false;
                        // console.log(successed);
                        // console.log("Error:" + response);
                    }
                );
            }
        });

        $scope.$emit('listChange');

        //default setting
        $scope.volumes = 100;
        $scope.curtTime = 0;
        $scope.player = $window.document.getElementById('playing');

        // communication (! receive) with sibling controllers by $rootScope.$on
        $rootScope.$on('modelChanged', function () {
            // console.log(DataShare.trick);
            // console.log(list);

            //before require list, Clear list first
            list = [];
            var val = $scope.$emit('listChange');
            console.log(val);
        });


        //when click href, ng-click do first;
        $scope.linkChange = function () {
            if ($scope.switch === 'play/content') {
                $scope.switch = 'now';
                // console.log($scope.switch);
            } else {
                $scope.switch = 'play/content';
                // console.log($scope.switch);
            }
        };

        //angular input ngModel value doesn't update  but do work in view (html) !?
        //volume
        // $scope.$watch('volumes',function () {
        //     console.log($scope.volumes);
        //     $scope.player.volume = $scope.volumes/100;
        // });
        $scope.volumeChanged = function () {
            var volume = document.getElementById('vol').value;
            $scope.player.volume = volume/100;
        };

        //load song, note $on, $emit about parameters passing
        // $scope.$emit('eventName', params); $scope.$on('eventName', function(event, params){});
        $scope.$on('load', function (event, song) {
            $scope.imagePath = hosturl + song.coverurl;
            $scope.player.src = hosturl + song.fileurl;
            $scope.musicinfo = song;
        });

        //update progress
        $scope.$watch('curtPercent',function () {
            console.log('progress');
            document.getElementById('progress_exp').MaterialProgress.setProgress($scope.curtPercent);
        });

        $scope.$on('loadRst', function () {
            var song = list.shift();
            $scope.$emit('load', song);
        });

        $scope.playpause = function toggling () {
            if ( $scope.player.paused == true  ) {
                document.getElementById('play').style.display = "none";
                document.getElementById('pause').style.display = "";
                $scope.player.play();

                $interval(function(){
                    $scope.curtTime = $scope.player.currentTime;
                    $scope.curtPercent = $scope.curtTime/$scope.musicinfo.length*100;
                    if ($scope.player.ended === true) {
                        var song = list.shift();
                        $scope.$emit('load', song);
                        $scope.player.play();
                        $scope.$emit('listChange');
                    }
                },200);
            }
            else if ( $scope.player.paused == false ) {
                document.getElementById('play').style.display = "";
                document.getElementById('pause').style.display = "none";
                $scope.player.pause();
            }
        };

        $scope.nexting = function next () {
            var flag233 = $scope.player.paused;
            $scope.player.pause();
            // console.log(flag233);
            var song = list.shift();
            // console.log(song);
            $scope.$emit('load', song);
            if (flag233 == false) {
                $scope.player.play();
            }
            // console.log($scope.player.volume);
            $scope.$emit('listChange');
        };

        $scope.repeat = function repeating () {
            if ($scope.player.loop == false) {
                document.getElementById('repeat-one').style.display = "";
                document.getElementById('repeat').style.display = "none";
                $scope.player.loop = true;
            } else if ($scope.player.loop == true) {
                document.getElementById('repeat-one').style.display = "none";
                document.getElementById('repeat').style.display = "";
                $scope.player.loop = false;
            }
        };

        $scope.matching = function matched ( keypressEvent) {

            var search;
            if (keypressEvent.keyCode === 13) {
                console.log('enter');
                var a = $scope.factor.split(' ');
                for (var i = 0; i < a.length;i++) {
                    var b = a[i].split(':');
                    console.log(b);
                    // var d = '"' + b[0] + '"';
                    var d = b[0];
                    for (var j = 1; j < b.length; j++) {
                        d = d + ':' + '"' + b[j] + '"';
                    }
                    if (i === 0) {
                        search = d;
                    } else {
                        search = search + ' ,' + d;
                    }
                }

                search = '{verb:' + '"' + 'list' + '"' + ', ' + search + '}';

                //string to object
                var obj = eval('(' + search + ')');
                // console.log(obj);
                // console.log(search);

                DataShare.trick = obj;
                // console.log(DataShare.trick);
                DataShare.model = 'list';
                // console.log(list);
                list = [];
                $scope.$emit('listChange');

            }
        };


        //setting recommendation cover
        $scope.rcd = {
            'hosturl': hosturl,
            'popular': undefined,
            'classical': undefined,
            'all': undefined,
            'soundtrack': undefined,
            'chinese': undefined,
            'cover': {
                'popular': undefined,
                'classical': undefined,
                'all': undefined,
                'soundtrack': undefined,
                'chinese': undefined
            }
        };

        ResGet.get({verb: 'list', type: 'Popular'},
            function success (response) {
                // console.log("RCD:" + JSON.stringify(response));
                $scope.rcd.popular = response;
                // console.log($scope.rcd);
            },
            function error (response) {
                console.log("Error:" + response);
            }
        );

        ResGet.get({verb: 'list', type: 'Classical'},
            function success (response) {
                // console.log("RCD:" + JSON.stringify(response));
                $scope.rcd.classical = response;
                // console.log($scope.rcd);
            },
            function error (response) {
                console.log("Error:" + response);
            }
        );

        ResGet.get({verb: 'list'},
            function success (response) {
                // console.log("RCD:" + JSON.stringify(response));
                $scope.rcd.all = response;
                // console.log($scope.rcd);
            },
            function error (response) {
                console.log("Error:" + response);
            }
        );

        ResGet.get({verb: 'list', type: 'Soundtrack'},
            function success (response) {
                // console.log("RCD:" + JSON.stringify(response));
                $scope.rcd.soundtrack = response;
                // console.log($scope.rcd);
            },
            function error (response) {
                console.log("Error:" + response);
            }
        );

        ResGet.get({verb: 'list', country: 'Chinese'},
            function success (response) {
                // console.log("RCD:" + JSON.stringify(response));
                $scope.rcd.chinese = response;
                // console.log($scope.rcd);
                $scope.$emit('loadCover');
            },
            function error (response) {
                console.log("Error:" + response);
            }
        );

        $scope.$on('loadCover',function () {
            SongGet.get({verb: 'meta', rawhash: $scope.rcd.popular[0].rawhash},
                function success (response) {
                    // console.log("cover_popular" + JSON.stringify(response));
                    $scope.rcd.cover.popular = response;
                    // console.log($scope.rcd);
                },
                function error (response) {
                    console.log("Error:" + response);
                }
            );

            SongGet.get({verb: 'meta', rawhash: $scope.rcd.classical[0].rawhash},
                function success (response) {
                    // console.log("cover_classical" + JSON.stringify(response));
                    $scope.rcd.cover.classical = response;
                    // console.log($scope.rcd);
                },
                function error (response) {
                    console.log("Error:" + response);
                }
            );

            SongGet.get({verb: 'meta', rawhash: $scope.rcd.all[0].rawhash},
                function success (response) {
                    // console.log("cover_all" + JSON.stringify(response));
                    $scope.rcd.cover.all = response;
                    // console.log($scope.rcd);
                },
                function error (response) {
                    console.log("Error:" + response);
                }
            );

            SongGet.get({verb: 'meta', rawhash: $scope.rcd.soundtrack[0].rawhash},
                function success (response) {
                    // console.log("cover_soundtrack" + JSON.stringify(response));
                    $scope.rcd.cover.soundtrack = response;
                    // console.log($scope.rcd);
                },
                function error (response) {
                    console.log("Error:" + response);
                }
            );

            SongGet.get({verb: 'meta', rawhash: $scope.rcd.chinese[0].rawhash},
                function success (response) {
                    // console.log("cover_chinese" + JSON.stringify(response));
                    $scope.rcd.cover.chinese = response;
                    // console.log($scope.rcd);
                },
                function error (response) {
                    console.log("Error:" + response);
                }
            );
        });

    }
]);

var albumControllers = angular.module('albumControllers',[]);

albumControllers.controller('AlbumsList',['AlbumGet','$scope',
    function (AlbumGet,$scope) {
        $scope.items = [];
        AlbumGet.save(function success (response) {
            console.log('Success :' + JSON.stringify(response));
            $scope.items = response;
            console.log('ITERMS:' + $scope.items);
        }, function error (response) {
           console.log('Error:' + response);
        });
    }    
]);

musicPlayerControllers.controller('Content', ['$scope','DataShare','$routeParams',
    function ($scope, DataShare, $routeParams) {
    }
]);

musicPlayerControllers.controller('Recommendation', ['$rootScope','$scope','ResGet','SongGet','DataShare',
    function ($rootScope ,$scope, ResGet, SongGet, DataShare) {

        $scope.popularSwitch = function () {

            //setting url params
            DataShare.trick = { verb: 'list' ,type: 'Popular'};
            DataShare.model = 'popular';

            // communication (! broadcast) with sibling controllers by $rootScope.$broadcast
            $rootScope.$broadcast('modelChanged');
        };

        $scope.ChineseSwitch = function () {
            DataShare.trick = { verb: 'list' ,country: 'Chinese'};
            DataShare.model = 'chinese';

            $rootScope.$broadcast('modelChanged');
        };

        $scope.classicalSwitch = function () {
            DataShare.trick = { verb: 'list' ,type: 'Classical'};
            DataShare.model = 'popular';

            $rootScope.$broadcast('modelChanged');
        };

        $scope.allSwitch = function () {
            DataShare.trick = { verb: 'list'};
            DataShare.model = 'all';

            $rootScope.$broadcast('modelChanged');
        };

        $scope.soundtrackSwitch = function () {
            DataShare.trick = { verb: 'list', type: 'Soundtrack'};
            DataShare.model = 'Soundtrack';

            $rootScope.$broadcast('modelChanged');
        };

        $scope.album = {
            value: false
        };

        $scope.$watch('album.value', function () {
            if ($scope.album.value === true) {
                // console.log(DataShare.trick);
                var obj = {method: 'album'};
                DataShare.trick = Object.assign(DataShare.trick, obj);
                // console.log(DataShare.trick);
                $rootScope.$broadcast('modelChanged');
            }
        })
    }
]);