//featured service slider
new Swiper('.card-wrapper', {
    loop: true,
    spaceBetween: 30,
    // Pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true, // Makes pagination bullets clickable
      dynamicBullets: true
    },

    // automatic slide
    autoplay: {
        delay: 3000,
        disableOnInteraction: false, // Continue autoplay after user interactions
      },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  
    // Breakpoints for responsive behavior
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 3,
      },
      1024: {
        slidesPerView: 4,
      },
    },
  });
  