<template>
  <div class="bg-white text-slate-900 overflow-x-hidden">
    <AppHeader />
    <HeroSection />
    <FeaturesSection />
    <HowItWorksSection />
    <PathwaysSection />
    <AboutSection />
    <CtaBanner />
    <LandingFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import HowItWorksSection from '@/components/landing/HowItWorksSection.vue'
import PathwaysSection from '@/components/landing/PathwaysSection.vue'
import AboutSection from '@/components/landing/AboutSection.vue'
import CtaBanner from '@/components/landing/CtaBanner.vue'
import LandingFooter from '@/components/landing/LandingFooter.vue'
</script>
