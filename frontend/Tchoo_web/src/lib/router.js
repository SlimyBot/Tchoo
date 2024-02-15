import { createRouter, createWebHistory } from "vue-router";
import { isLoggedIn, isTeacher } from "./auth.js";
import MainPage from "../components/pages/MainPage.vue";

const routes = [
  {
    path: "/",
    name: "mainPage",
    component: MainPage,
  },
  {
    path: "/casLogin/:ticket?",
    name: "casLogin",
    component: () => import("../components/pages/SSOCasLogin.vue"),
  },
  {
    path: "/surveys",
    name: "surveys",
    component: () => import("../components/pages/AllSurveys.vue"),
  },
  {
    path: "/results",
    name: "results",
    component: () => import("../components/pages/studentPage.vue"),
  },
  {
    path: "/join",
    name: "join",
    component: () => import("../components/pages/session/JoinGame.vue")
  },
  {
    path: "/session/:joinCode",
    name: "session",
    component: () => import("../components/pages/session/InSession.vue")
  },
  {
    path: "/survey/:id",
    name: "survey",
    component: () => import("../components/pages/Create.vue"),
  },
  {
    path: "/createChoice",
    name: "createChoice",
    component: () => import("../components/pages/CreateChoice.vue"),
  },
  {
    path: "/groups",
    name: "groups",
    component: () => import("../components/pages/AllGroups.vue"),
  },
  {
    path: "/group/:id",
    name: "group",
    component: () => import("../components/pages/Group.vue"),
  },
  {
    path: "/:catchAll(.*)",
    name: "Not Found",
    component: () => import("../components/pages/404.vue"),
  },
  {
    path: "/endSurvey/:join_code",
    name: "EndSurvey",
    component: () => import("../components/pages/EndSurvey.vue"),
  },
  {
    path: "/endSurvey/:id_player/:join_code",
    name: "ResultSession",
    component: () => import("../components/pages/ResultsPlayer.vue"),
  },
  {
    path: "/template/:id",
    name: "CreateSession",
    component: () => import("../components/pages/session/CreateSession.vue"),
  },
  {
    path: "/allSessions",
    name: "AllSessions",
    component: () => import("../components/pages/session/AllSessions.vue"),
  },
  {
    path: "/createQuestion/:id",
    name: "createQuestion",
    component: () => import("../components/pages/CreateQuestion.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/// Concerne le auth_guard

// Les routes ou si on est connecté il n'y a pas besoin d'être dessus
const GOTO_MAIN_PAGE = ["/", "/login", "/casLogin"];

router.beforeEach((to, from, next) => {
  if (GOTO_MAIN_PAGE.includes(to.path) && isLoggedIn()) {
    if (isTeacher()) {
      next("/surveys");
    } else {
      next("/results");
    }

  } else {
    next();
  }
});
export default router;
