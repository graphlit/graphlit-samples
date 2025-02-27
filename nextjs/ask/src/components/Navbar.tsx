'use client';

import * as React from 'react';
import Image from 'next/image';
import NextLink from 'next/link';
import {
  NavbarBrand,
  NavbarContent,
  Navbar as NextUINavbar,
} from '@nextui-org/navbar';
import { Tooltip } from '@nextui-org/tooltip';

import { DiscordIcon } from '@/components/icons/DiscordIcon';
import { GithubIcon } from '@/components/icons/GithubIcon';

export function Navbar() {
  return (
    <NextUINavbar maxWidth="full" position="sticky" isBordered>
      {/* Navbar content for the brand */}
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex justify-start items-center gap-1" href="/">
            <Image
              src="/images/graphlit-logo.svg"
              width={40}
              height={20}
              alt="Graphlit logo"
            />
            <p className="font-bold text-inherit">Graphlit</p>
          </NextLink>
        </NavbarBrand>
      </NavbarContent>

      {/* Navbar content for external links */}
      <NavbarContent
        className="hidden sm:flex basis-1/5 sm:basis-full"
        justify="end"
      >
        <Tooltip content="Join our Discord community">
          <NextLink
            target="_blank"
            aria-label="Discord"
            className="mr-3"
            href="https://discord.gg/ygFmfjy3Qx"
          >
            <DiscordIcon className="text-default-500" />
          </NextLink>
        </Tooltip>
        <Tooltip content="View source on GitHub">
          <NextLink
            target="_blank"
            aria-label="Github"
            href="https://github.com/graphlit/graphlit-samples/tree/main/nextjs/ask"
          >
            <GithubIcon className="text-default-500" />
          </NextLink>
        </Tooltip>
      </NavbarContent>
    </NextUINavbar>
  );
}
