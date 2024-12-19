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


new Swiper('.testimonials-wrapper', {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 20,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      

      // automatic slide
    autoplay: {
        delay: 3000,
        disableOnInteraction: false, // Continue autoplay after user interactions
      },
      breakpoints: {
        640: {
          slidesPerView: 1,
          spaceBetween: 10
        },
        768: {
          slidesPerView: 2,
          spaceBetween: 20
        },
        1024: {
          slidesPerView: 3,
          spaceBetween: 30
        }
      }
  });
  
 
  