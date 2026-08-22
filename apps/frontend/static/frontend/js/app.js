(function () {
  // Переключатель урока: 'token' или 'jwt'. Смотри заголовок Authorization в Network.
  const MODE_KEY = 'vewsets_auth_mode';
  const TOKEN_KEY = 'vewsets_token';
  const ACCESS_KEY = 'vewsets_access';
  const REFRESH_KEY = 'vewsets_refresh';
  const PROFILE_KEY = 'vewsets_profile';
  const HINTS = {
    token: 'Заголовок: Authorization: Token <ключ>. Ключ лежит в таблице authtoken_token.',
    jwt: 'Заголовок: Authorization: Bearer <access>. Access короткий, refresh выдаёт новый.',
  };

  function getAuthMode() {
    return localStorage.getItem(MODE_KEY) || 'token';
  }

  function setAuthMode(mode) {
    localStorage.setItem(MODE_KEY, mode);
  }

  function loginUrl() {
    return getAuthMode() === 'jwt'
      ? '/users/login/jwt/'
      : '/users/login/token/';
  }

  function bindAuthModeSelect() {
    const select = document.querySelector('#auth-mode');
    if (!select) {
      return;
    }
    select.value = getAuthMode();
    const hint = document.querySelector('#auth-hint');
    function sync() {
      setAuthMode(select.value);
      if (hint) {
        hint.textContent = HINTS[select.value];
      }
    }
    sync();
    select.addEventListener('change', sync);
  }

  const api = {
    profile() {
      try {
        return JSON.parse(localStorage.getItem(PROFILE_KEY));
      } catch (err) {
        return null;
      }
    },
    isLoggedIn() {
      if (getAuthMode() === 'jwt') {
        return Boolean(localStorage.getItem(ACCESS_KEY));
      }
      return Boolean(localStorage.getItem(TOKEN_KEY));
    },
    persist(data) {
      localStorage.setItem(PROFILE_KEY, JSON.stringify(data.profile));
      if (getAuthMode() === 'jwt') {
        localStorage.setItem(ACCESS_KEY, data.access);
        localStorage.setItem(REFRESH_KEY, data.refresh);
        localStorage.removeItem(TOKEN_KEY);
        return;
      }
      localStorage.setItem(TOKEN_KEY, data.token);
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);
    },
    clear() {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);
      localStorage.removeItem(PROFILE_KEY);
    },
    authValue() {
      if (getAuthMode() === 'jwt') {
        const access = localStorage.getItem(ACCESS_KEY);
        return access ? 'Bearer ' + access : '';
      }
      const token = localStorage.getItem(TOKEN_KEY);
      return token ? 'Token ' + token : '';
    },
    headers(isJson) {
      const headers = {};
      if (isJson) {
        headers['Content-Type'] = 'application/json';
      }
      const authorization = this.authValue();
      if (authorization) {
        headers.Authorization = authorization;
      }
      return headers;
    },
    async refreshJwt() {
      const refresh = localStorage.getItem(REFRESH_KEY);
      if (!refresh) {
        return false;
      }
      const response = await fetch('/users/login/jwt/refresh/', {
        method: 'POST',
        credentials: 'omit',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refresh }),
      });
      if (!response.ok) {
        return false;
      }
      const data = await response.json();
      localStorage.setItem(ACCESS_KEY, data.access);
      if (data.refresh) {
        localStorage.setItem(REFRESH_KEY, data.refresh);
      }
      return true;
    },
    async request(url, options) {
      const opts = options || {};
      const isForm = opts.body instanceof FormData;
      const response = await fetch(url, {
        credentials: 'omit',
        ...opts,
        headers: {
          ...this.headers(!isForm),
          ...(opts.headers || {}),
        },
      });
      // JWT: access протух → один раз берём новый по refresh и повторяем запрос.
      if (
        response.status === 401 &&
        getAuthMode() === 'jwt' &&
        !opts._retry
      ) {
        const refreshed = await this.refreshJwt();
        if (refreshed) {
          return this.request(url, { ...opts, _retry: true });
        }
      }
      if (response.status === 204) {
        return null;
      }
      const data = await response.json().catch(function () {
        return null;
      });
      if (!response.ok) {
        const error = new Error(formatError(data));
        error.status = response.status;
        throw error;
      }
      return data;
    },
  };

  function formatError(data) {
    if (!data) {
      return 'Ошибка запроса';
    }
    if (typeof data.detail === 'string') {
      return data.detail;
    }
    return Object.keys(data)
      .map(function (key) {
        return key + ': ' + [].concat(data[key]).join(', ');
      })
      .join('\n');
  }

  function qs(selector) {
    return document.querySelector(selector);
  }

  function fileUrl(path) {
    if (!path) {
      return '';
    }
    if (path.indexOf('http') === 0 || path.indexOf('/') === 0) {
      return path;
    }
    return '/media/' + path;
  }

  function isManager(profile) {
    return Boolean(profile && profile.role === 'manager');
  }

  function isVerified(profile) {
    return Boolean(profile && profile.is_verified);
  }

  function roleText(profile) {
    if (!profile) {
      return 'Гость';
    }
    if (isManager(profile)) {
      return 'Менеджер';
    }
    if (isVerified(profile)) {
      return 'Верифицирован';
    }
    return 'Ожидает верификации';
  }

  function showFlash(message, ok) {
    const box = qs('#flash');
    if (!box) {
      return;
    }
    box.hidden = false;
    box.textContent = message;
    box.classList.toggle('ok', Boolean(ok));
  }

  function empty(node, text) {
    node.innerHTML = '<p class="empty">' + text + '</p>';
  }

  function renderNav() {
    const box = qs('#nav-auth');
    if (!box) {
      return;
    }
    const profile = api.profile();
    if (!profile) {
      box.innerHTML =
        '<a class="btn ghost" href="/login/">Вход</a>' +
        '<a class="btn" href="/register/">Регистрация</a>';
      return;
    }
    let extra = '<a class="btn ghost" href="/profile/">' + profile.username + '</a>';
    if (isManager(profile)) {
      extra += '<a class="btn" href="/manager/">Кабинет</a>';
    }
    box.innerHTML = extra;
  }

  async function loadFooter() {
    const box = qs('#site-footer');
    try {
      const items = await api.request('/header-footer/footer/');
      if (!items || !items.length) {
        return;
      }
      const footer = items[0];
      const texts = footer.footer_text_detail || {};
      box.innerHTML =
        '<div><strong>' +
        (footer.title || 'Vewsets') +
        '</strong><p>' +
        (footer.description || '') +
        '</p></div><p>' +
        [texts.title1, texts.title2, texts.title3, texts.title4]
          .filter(Boolean)
          .join(' · ') +
        '</p>';
    } catch (err) {
      return;
    }
  }

  function projectCard(item) {
    const img = fileUrl(item.image);
    return (
      '<article class="card">' +
      (img ? '<img src="' + img + '" alt="">' : '<div class="thumb"></div>') +
      '<div class="card-body"><p class="muted">' +
      (item.category || '') +
      '</p><h3>' +
      item.title +
      '</h3><p class="muted">' +
      (item.author || '') +
      '</p></div></article>'
    );
  }

  function courseCard(item) {
    return (
      '<a class="card" href="/courses/' +
      item.id +
      '/"><div class="card-body"><p class="muted">' +
      (item.is_published ? 'Опубликован' : 'Черновик') +
      '</p><h3>' +
      (item.title || 'Курс #' + item.id) +
      '</h3><p class="muted">' +
      (item.description || '') +
      '</p></div></a>'
    );
  }

  function postCard(item) {
    return (
      '<a class="row-card" href="/posts/' +
      item.id +
      '/"><div><h3>' +
      item.title +
      '</h3><p class="muted">' +
      (item.category_name || '') +
      '</p></div><span>→</span></a>'
    );
  }

  async function renderProjects(list) {
    const items = await api.request('/api/projects/');
    if (!items.length) {
      empty(list, 'Проектов пока нет.');
      return;
    }
    list.innerHTML = items.map(projectCard).join('');
  }

  async function renderCourses(list) {
    const items = await api.request('/course/courses/');
    if (!items.length) {
      empty(list, 'Курсов пока нет.');
      return;
    }
    list.innerHTML = items.map(courseCard).join('');
  }

  async function renderPosts(list) {
    const payload = await api.request('/blog/blog/');
    const items = payload.results || payload;
    if (!items.length) {
      empty(list, 'Постов пока нет.');
      return;
    }
    list.innerHTML = items.map(postCard).join('');
  }

  async function initHome() {
    try {
      const headers = await api.request('/header-footer/header/');
      const header = headers && headers[0];
      if (header) {
        qs('#hero-title').textContent = header.title;
        qs('#hero-stats').innerHTML =
          '<div class="stat"><b>' +
          header.followers +
          '</b><span>подписчики</span></div>' +
          '<div class="stat"><b>' +
          header.users +
          '</b><span>пользователи</span></div>';
      }
    } catch (err) {
      showFlash(err.message);
    }
    const [projects, courses, posts] = await Promise.all([
      api.request('/api/projects/'),
      api.request('/course/courses/'),
      api.request('/blog/blog/'),
    ]);
    const projectBox = qs('#home-projects');
    const courseBox = qs('#home-courses');
    const postBox = qs('#home-posts');
    const projectItems = (projects || []).slice(0, 3);
    const courseItems = (courses || []).slice(0, 3);
    const postItems = (posts.results || posts || []).slice(0, 3);
    projectBox.innerHTML = projectItems.map(projectCard).join('') || '';
    courseBox.innerHTML = courseItems.map(courseCard).join('') || '';
    postBox.innerHTML = postItems.map(postCard).join('') || '';
    if (!projectItems.length) {
      empty(projectBox, 'Проектов пока нет.');
    }
    if (!courseItems.length) {
      empty(courseBox, 'Опубликованных курсов нет.');
    }
    if (!postItems.length) {
      empty(postBox, 'Постов пока нет.');
    }
  }

  async function initProjects() {
    const list = qs('#project-list');
    await renderProjects(list);
    if (!isManager(api.profile())) {
      return;
    }
    qs('#project-form-wrap').hidden = false;
    qs('#project-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        await api.request('/api/projects/', {
          method: 'POST',
          body: new FormData(form),
        });
        showFlash('Проект создан.', true);
        form.reset();
        await renderProjects(list);
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  async function initCourses() {
    const list = qs('#course-list');
    await renderCourses(list);
    if (!isManager(api.profile())) {
      return;
    }
    qs('#course-form-wrap').hidden = false;
    qs('#course-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      const body = {
        title: form.title.value,
        description: form.description.value,
        students_count: Number(form.students_count.value || 0),
        link: form.link.value || 'https://example.com',
        is_published: form.is_published.checked,
      };
      try {
        await api.request('/course/courses/', {
          method: 'POST',
          body: JSON.stringify(body),
        });
        showFlash('Курс создан.', true);
        form.reset();
        await renderCourses(list);
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  async function loadCoursePage(courseId) {
    const box = qs('#course-box');
    const course = await api.request('/course/courses/' + courseId + '/');
    box.innerHTML =
      '<p class="badge">' +
      (course.is_published ? 'Опубликован' : 'Черновик') +
      '</p><h1>' +
      course.title +
      '</h1><p>' +
      course.description +
      '</p>';
    document.title = course.title + ' · Vewsets';
    const lessons = await api.request(
      '/course/courses/' + courseId + '/lessons/',
    );
    const list = qs('#lesson-list');
    if (!lessons.length) {
      empty(list, 'Уроков пока нет.');
      return;
    }
    list.innerHTML = lessons
      .map(function (item) {
        return (
          '<article class="row-card"><div><h3>' +
          item.title +
          '</h3><p class="muted">' +
          item.duration_min +
          ' мин</p><p>' +
          item.content +
          '</p></div></article>'
        );
      })
      .join('');
  }

  async function initCourseDetail() {
    const box = qs('#course-box');
    const courseId = box.dataset.id;
    try {
      await loadCoursePage(courseId);
    } catch (err) {
      box.innerHTML = '<p class="empty">Курс недоступен.</p>';
      return;
    }
    if (!isManager(api.profile())) {
      return;
    }
    qs('#lesson-form-wrap').hidden = false;
    qs('#lesson-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      const body = {
        title: form.title.value,
        content: form.content.value,
        duration_min: Number(form.duration_min.value),
        order: Number(form.order.value),
      };
      try {
        await api.request('/course/courses/' + courseId + '/lessons/', {
          method: 'POST',
          body: JSON.stringify(body),
        });
        showFlash('Урок добавлен.', true);
        form.reset();
        await loadCoursePage(courseId);
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  async function initBlog() {
    const list = qs('#post-list');
    await renderPosts(list);
    if (!isVerified(api.profile())) {
      return;
    }
    const categories = await api.request('/blog/category/');
    const select = qs('#post-category');
    select.innerHTML = categories
      .map(function (item) {
        return '<option value="' + item.id + '">' + item.name + '</option>';
      })
      .join('');
    if (!categories.length) {
      showFlash('Сначала менеджер должен создать категорию.');
      return;
    }
    qs('#post-form-wrap').hidden = false;
    qs('#post-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      const body = {
        title: form.title.value,
        content: form.content.value,
        category: Number(form.category.value),
      };
      try {
        await api.request('/blog/blog/', {
          method: 'POST',
          body: JSON.stringify(body),
        });
        showFlash('Пост опубликован.', true);
        form.reset();
        await renderPosts(list);
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  async function initBlogDetail() {
    const box = qs('#post-box');
    try {
      const post = await api.request('/blog/blog/' + box.dataset.id + '/');
      box.innerHTML =
        '<p class="muted">' +
        (post.category_name || '') +
        '</p><h1>' +
        post.title +
        '</h1><p>' +
        post.content +
        '</p>';
      document.title = post.title + ' · Vewsets';
    } catch (err) {
      box.innerHTML = '<p class="empty">Пост не найден.</p>';
    }
  }

  async function enterWithPassword(username, password) {
    const data = await api.request(loginUrl(), {
      method: 'POST',
      body: JSON.stringify({ username: username, password: password }),
    });
    api.persist(data);
  }

  function bindLoginForm() {
    bindAuthModeSelect();
    qs('#login-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        await enterWithPassword(form.username.value, form.password.value);
        showFlash('Вход выполнен (' + getAuthMode() + ').', true);
        window.location.href = '/profile/';
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  function bindRegisterForm() {
    bindAuthModeSelect();
    qs('#register-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      const payload = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
      };
      try {
        await api.request('/users/register/', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        await enterWithPassword(payload.username, payload.password);
        showFlash('Аккаунт создан, вход через ' + getAuthMode() + '.', true);
        window.location.href = '/profile/';
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  async function initProfile() {
    const box = qs('#profile-box');
    if (!api.isLoggedIn()) {
      window.location.href = '/login/';
      return;
    }
    try {
      const profile = await api.request('/users/me/');
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
      const mode = getAuthMode();
      box.innerHTML =
        '<h1>' +
        profile.username +
        '</h1><p class="badge">' +
        roleText(profile) +
        '</p><p class="muted">Сейчас вход: ' +
        (mode === 'jwt' ? 'JWT (Bearer)' : 'Token') +
        '</p><p class="muted">' +
        (profile.email || 'email не указан') +
        '</p><p>' +
        (isVerified(profile)
          ? 'Можно писать в блог.'
          : 'Менеджер ещё не верифицировал аккаунт — запись в блог закрыта.') +
        '</p><button id="logout-btn" type="button">Выйти</button>';
      qs('#logout-btn').addEventListener('click', async function () {
        try {
          if (mode === 'token') {
            await api.request('/users/logout/token/', { method: 'POST' });
          }
        } catch (err) {
          return;
        } finally {
          api.clear();
          window.location.href = '/';
        }
      });
    } catch (err) {
      api.clear();
      window.location.href = '/login/';
    }
  }

  async function renderUsers(list) {
    const users = await api.request('/users/');
    list.innerHTML = users
      .map(function (item) {
        const action = item.is_verified
          ? '<span class="badge">верифицирован</span>'
          : '<button data-verify="' + item.id + '">Верифицировать</button>';
        return (
          '<article class="row-card"><div><h3>' +
          item.username +
          '</h3><p class="muted">' +
          item.role +
          '</p></div>' +
          action +
          '</article>'
        );
      })
      .join('');
  }

  async function initManager() {
    if (!isManager(api.profile())) {
      showFlash('Кабинет только для менеджера.');
      window.location.href = '/';
      return;
    }
    const list = qs('#user-list');
    await renderUsers(list);
    list.addEventListener('click', async function (event) {
      const id = event.target.getAttribute('data-verify');
      if (!id) {
        return;
      }
      try {
        await api.request('/users/' + id + '/verify/', { method: 'POST' });
        showFlash('Пользователь верифицирован.', true);
        await renderUsers(list);
      } catch (err) {
        showFlash(err.message);
      }
    });

    qs('#category-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        await api.request('/blog/category/', {
          method: 'POST',
          body: JSON.stringify({
            name: form.name.value,
            slug: form.slug.value,
          }),
        });
        showFlash('Категория создана.', true);
        form.reset();
      } catch (err) {
        showFlash(err.message);
      }
    });

    qs('#header-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        await api.request('/header-footer/header/', {
          method: 'POST',
          body: JSON.stringify({
            title: form.title.value,
            link: form.link.value,
            followers: Number(form.followers.value || 0),
            users: Number(form.users.value || 0),
            like: form.like.checked,
          }),
        });
        showFlash('Шапка сохранена.', true);
      } catch (err) {
        showFlash(err.message);
      }
    });

    qs('#footer-text-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        const created = await api.request('/header-footer/footer-text/', {
          method: 'POST',
          body: JSON.stringify({
            title1: form.title1.value,
            title2: form.title2.value,
            title3: form.title3.value,
            title4: form.title4.value,
          }),
        });
        qs('#footer-form [name="footer_text"]').value = created.id;
        showFlash('Тексты созданы. ID подставлен в форму подвала.', true);
      } catch (err) {
        showFlash(err.message);
      }
    });

    qs('#footer-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      try {
        await api.request('/header-footer/footer/', {
          method: 'POST',
          body: new FormData(form),
        });
        showFlash('Подвал создан.', true);
        loadFooter();
      } catch (err) {
        showFlash(err.message);
      }
    });
  }

  const page = document.body.dataset.page;
  renderNav();
  loadFooter();

  const loaders = {
    home: initHome,
    projects: initProjects,
    courses: initCourses,
    'course-detail': initCourseDetail,
    blog: initBlog,
    'blog-detail': initBlogDetail,
    login: function () {
      bindLoginForm();
    },
    register: function () {
      bindRegisterForm();
    },
    profile: initProfile,
    manager: initManager,
  };

  if (loaders[page]) {
    const result = loaders[page]();
    if (result && typeof result.catch === 'function') {
      result.catch(function (err) {
        showFlash(err.message || 'Не удалось загрузить данные.');
      });
    }
  }
})();
